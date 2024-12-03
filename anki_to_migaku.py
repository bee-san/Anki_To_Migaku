import requests
import json

ANKI_CONNECT_URL = "http://localhost:8765"

# Migaku card type

# Assumes your deck is called MiningNew under Japanese. Change this.
# Assumes you consider mature cards to have intervals >= 21 days
# Assumes your card type is Migaku
migaku_search_query = "deck:Default::Japanese::MiningNew prop:ivl>=21 card:Migaku*"
migaku_field_name = "Target_Word_Clean"

# Lapis card type
# Change according to above
lapis_search_query = "deck:Default::Japanese::MiningNew prop:ivl>=21 card:Mining*"
lapis_field_name = "Expression"

# kaishi needs quotes in its name due to having a space
kaishi_search_query = '"deck:Default::Japanese::Kaishi 1.5k" prop:ivl>=21'
kaishi_field_name = "Word"


output_file = "target_words.txt"


def anki_request(action, **params):
    payload = {"action": action, "version": 6, "params": params}
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    response.raise_for_status()
    return response.json()


def words_to_anki(f, search_query, field_name):
    try:
        # Find cards matching the search query
        print("Searching for cards...")
        card_ids_response = anki_request("findCards", query=search_query)
        card_ids = card_ids_response.get("result", [])

        if not card_ids:
            print("No cards found for the given query.")
            print("This script will find Migaku cards first, and then Lapis")

        # Fetch the card details
        print(f"Found {len(card_ids)} cards. Fetching card details...")
        card_info_response = anki_request("cardsInfo", cards=card_ids)
        card_info = card_info_response.get("result", [])

        # Extract words from the specified field
        words = []
        for card in card_info:
            fields = card.get("fields", {})
            target_word_clean = fields.get(field_name, {}).get("value", "").strip()
            if target_word_clean:
                words.append(target_word_clean)

        if not words:
            print("No words found in the specified field.")
            exit()

        # Write words to the output file
        print(f"Writing {len(words)} words to {output_file}...")
        f.write("\n".join(words))

        print("Words successfully written to the file.")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to AnkiConnect: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


f = open(output_file, "w", encoding="utf-8")
print("Migaku cards")
words_to_anki(f, migaku_search_query, migaku_field_name)
print("Lapis cards")
words_to_anki(f, lapis_search_query, lapis_field_name)
print("Kaishi cards")
words_to_anki(f, kaishi_search_query, kaishi_field_name)
f.close()
