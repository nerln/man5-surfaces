#!/usr/bin/env bash
# Re-derive the comparison figures in README.md from the public bucket.
#
#   ./public_areas.sh PHercMANBp
#   ./public_areas.sh PHerc0139
#   ./public_areas.sh PHerc0814
#
# No credentials, no aws CLI: anonymous HTTP against the open-data bucket. Needs
# curl and jq. Lists a scroll's published segments, reads area_cm2 from each
# segment's tifxyz_original metadata, and prints the per-segment areas followed
# by the count, total, min, max and median.
#
# Two choices are made here, and they are the ones the README states, because a
# reader who makes them differently will get different numbers:
#   - area comes from mesh/intermediate/tifxyz_original/meta.json. The sibling
#     tifxyz_normalized and tifxyz_flattened documents carry area_cm2: null.
#   - a segment that publishes no area is reported as NA and left out of the
#     statistics, rather than counted as zero.
#
# seed_surface_id is printed beside each area. There is no auto_grown field in
# this catalogue; that id is the only public record of what a surface was grown
# from, and it does not say how much hand work followed.

set -uo pipefail

BUCKET="https://vesuvius-challenge-open-data.s3.amazonaws.com"
SCROLL="${1:-PHercMANBp}"
JOBS="${JOBS:-12}"

command -v curl >/dev/null || { echo "curl is required" >&2; exit 2; }
command -v jq   >/dev/null || { echo "jq is required" >&2; exit 2; }

# delimiter=/ keeps the listing to segment prefixes. Without it the surface-volume
# zarr chunks are enumerated too, which is thousands of keys and will time out.
segments=$(
  curl -s --max-time 60 \
    "$BUCKET/?list-type=2&prefix=${SCROLL}/segments/&delimiter=/&max-keys=1000" \
  | grep -o '<Prefix>[^<]*</Prefix>' \
  | sed 's/<[^>]*>//g' \
  | grep -v "^${SCROLL}/segments/$"
)

if [ -z "$segments" ]; then
  echo "no segments listed for ${SCROLL}" >&2
  exit 1
fi

echo "# ${SCROLL}: $(printf '%s\n' "$segments" | wc -l | tr -d ' ') published segment directories"
echo

one() {
  prefix="$1"
  seg="${prefix#*/segments/}"; seg="${seg%/}"
  doc=$(curl -sf --max-time 30 "${BUCKET}/${prefix}mesh/intermediate/tifxyz_original/meta.json" || echo '{}')
  printf '%s\t%s\t%s\n' \
    "$(printf '%s' "$doc" | jq -r '.area_cm2   // "NA"')" \
    "$(printf '%s' "$doc" | jq -r '.seed_surface_id // "NA"')" \
    "$seg"
}
export -f one
export BUCKET

rows=$(printf '%s\n' "$segments" | xargs -P "$JOBS" -I{} bash -c 'one "$@"' _ {} | sort -g)

printf '%-22s  %-42s  %s\n' "area_cm2" "seed_surface_id" "segment"
printf '%s\n' "$rows" | awk -F'\t' '{printf "%-22s  %-42s  %s\n", $1, $2, $3}'

printf '%s\n' "$rows" | awk -F'\t' '
  $1 != "NA" { a[n++] = $1 + 0; s += $1 }
  END {
    if (n == 0) { print "\nno segment published an area"; exit }
    m = (n % 2) ? a[int(n/2)] : (a[n/2 - 1] + a[n/2]) / 2
    printf "\nwith area: %d    total: %.4f    min: %.4f    max: %.4f    median: %.4f\n", n, s, a[0], a[n-1], m
  }'
