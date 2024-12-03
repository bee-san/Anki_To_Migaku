# Anki Words to Migaku

Script that grabs mature cards from Anki and lets you put them into Migaku.

Requires:
*  Anki Connect in Anki
* Migaku addon https://ankiweb.net/shared/info/1846879528

**No support will be given. This works fine for me and I don't want to maintain this for other people. Feel free to fork and edit it for your own use!**

# Assumptions

You are using a Migaku card format that features `Target_Word_Clean`. You need this because Migaku words-known input can't read the expression details.

You can add this field to your current Migaku cards.

## Update existing cards

You can remove the syntax from current cards using Migaku anki addon.

And then mass-copy them over to another field using Advanced Copy Fields https://ankiweb.net/shared/info/1898445115

Then re-add the syntax.

## New cards

Change map_fields to put target_word (no syntax) into target_word_clean

## Usage

Have Anki open and run this:


`python3 anki_to_migaku.py`
