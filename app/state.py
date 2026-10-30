from typing import TypedDict


class State(TypedDict, total=False):
    raw_input: str      
    domain: str         
    main_domain: str    
    tld: str            
    ips: list[str]      
    error: str          
    answer: str         