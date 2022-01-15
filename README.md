# seagrind

## work-in-progress (?)

An attempt for a quick (and not so smart) webscraper of NFT png art collections off of opensea.io.

Created for learning purposes.

## How to use:
Pick your favorite NFT collection, find its associated contract address, and provide with a range of tokens.

Tokens range between `start_id` and `end_id`. (inclusive)

### Dependencies:
Python version >= 3.8
```bash
python -m venv venv
pip install requirements.txt
```

### Running the script:
```bash
python main.py -c $contract -s $start_id -e $end_id
```

## Disclaimers:
The script was tested on only a few collections at a single point of time.

opensea.io may change their interface and the script would be quickly rendered obsolete.

The script also relies on Firefox's geckodriver GitHub repository, and may be affected by any changes in their releases.
