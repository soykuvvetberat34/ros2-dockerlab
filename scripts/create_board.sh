#!/usr/bin/env bash
# docs/kartlar.md içindeki her "## Kart" bölümünü issue olarak açar,
# GitHub Projects panosuna ekler ve Status alanını "Yapılacak" yapar.
#
# Kullanım: ./scripts/create_board.sh <PROJE_NO> [OWNER]
set -euo pipefail

PROJECT_NO="${1:?Kullanım: $0 <PROJE_NO> [OWNER]}"
OWNER="${2:-@me}"
STATUS_NAME="Yapılacak"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"   # gh issue create bu deponun remote'unu kullansın
CARDS="$ROOT/docs/kartlar.md"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# kartlar.md dosyasını kart başına bir dosyaya böl
awk -v dir="$TMP" '
  /^## Kart / { n++; file = sprintf("%s/%02d.md", dir, n); print > file; next }
  n > 0       { print >> file }
' "$CARDS"

# Proje, Status alanı ve "Yapılacak" seçeneğinin kimliklerini bul
PROJECT_ID="$(gh project view "$PROJECT_NO" --owner "$OWNER" --format json --jq .id)"
FIELD_JSON="$(gh project field-list "$PROJECT_NO" --owner "$OWNER" --format json)"
STATUS_FIELD_ID="$(jq -r '.fields[] | select(.name=="Status") | .id' <<<"$FIELD_JSON")"
OPTION_ID="$(jq -r --arg s "$STATUS_NAME" \
  '.fields[] | select(.name=="Status") | .options[] | select(.name==$s) | .id' <<<"$FIELD_JSON")"

if [[ -z "$OPTION_ID" ]]; then
  echo "HATA: Status alanında '$STATUS_NAME' seçeneği yok." >&2
  exit 1
fi

for card in "$TMP"/*.md; do
  title="$(head -n1 "$card" | sed -E 's/^## Kart [0-9]+: //')"
  body="$(tail -n +2 "$card" | sed -e '/./,$!d')"

  url="$(gh issue create --title "$title" --body "$body")"
  echo "Issue açıldı: $url"

  item_id="$(gh project item-add "$PROJECT_NO" --owner "$OWNER" --url "$url" --format json --jq .id)"
  gh project item-edit --id "$item_id" --project-id "$PROJECT_ID" \
    --field-id "$STATUS_FIELD_ID" --single-select-option-id "$OPTION_ID" >/dev/null
  echo "  -> panoya eklendi, Status: $STATUS_NAME"
done
