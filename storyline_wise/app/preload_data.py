import pandas as pd
from typing import Optional
from dotenv import load_dotenv

from storyline_wise.query import Snowflake

from storyline.common.utils import cached_call
from storyline.common.hash import hash_string

from wise_chain.init_defaults import init_motleycrew_defaults

# This makes sure we call the LLM gateway LLMs
init_motleycrew_defaults("Egor Kraev", "Report helper")

sf = Snowflake()


def cached_load(query: str, cache_dir: Optional[str] = None) -> pd.DataFrame:
    fn = f"{hash_string(query)}.pkl"
    if cache_dir:
        fn = f"{cache_dir}/{fn}"
    df = cached_call(lambda: sf.execute(query), fn)
    return df
