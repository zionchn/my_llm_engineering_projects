import json
import pandas as pd


# Clean the function incase the json output is not clean
def clean_json(raw_content):
    cleaned = (raw_content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip())

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        try:
            return json.loads(cleaned[cleaned.find('['):cleaned.rfind(']') + 1])
        except Exception:
            raise json.JSONDecodeError("Could not isolate JSON Structure", raw_content, 0)


# Create a DafaFrame
def create_dataframe(raw_content):
    data = clean_json(raw_content)
    print("Successfully turned into a python object:", type(data))

    df = pd.DataFrame(data)
    return df
