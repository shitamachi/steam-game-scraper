from typing import List, Dict, Any, Optional, TypedDict

class PriceOverview(TypedDict):
    currency: str
    initial: int
    final: int
    discount_percent: int
    initial_formatted: str
    final_formatted: str

class PlatformRequirements(TypedDict):
    minimum: str
    recommended: str

class Category(TypedDict):
    id: int
    description: str

class Genre(TypedDict):
    id: str
    description: str

class Screenshot(TypedDict):
    id: int
    path_thumbnail: str
    path_full: str

class Movie(TypedDict):
    id: int
    name: str
    thumbnail: str
    webm: Dict[str, str]
    mp4: Dict[str, str]
    highlight: bool

class Recommendation(TypedDict):
    total: int

class Achievement(TypedDict):
    name: str
    path: str

class Achievements(TypedDict):
    total: int
    highlighted: List[Achievement]

class ReleaseDate(TypedDict):
    coming_soon: bool
    date: str

class SupportInfo(TypedDict):
    url: str
    email: str

class ContentDescriptors(TypedDict):
    ids: List[int]
    notes: str

class Rating(TypedDict):
    rating: str
    descriptors: str
    required_age: str
    use_age_gate: str
    banned: Optional[str] # Only for steam_germany
    rating_generated: Optional[str] # Only for steam_germany

class AppDetailsData(TypedDict):
    type: str
    name: str
    steam_appid: int
    required_age: str
    is_free: bool
    controller_support: str
    dlc: List[int]
    detailed_description: str
    about_the_game: str
    short_description: str
    supported_languages: str
    header_image: str
    capsule_image: str
    capsule_imagev5: str
    website: Optional[str]
    pc_requirements: PlatformRequirements
    mac_requirements: PlatformRequirements
    linux_requirements: PlatformRequirements
    legal_notice: str
    developers: List[str]
    publishers: List[str]
    price_overview: Optional[PriceOverview]
    packages: List[int]
    package_groups: List[Any] # This can be complex, using Any for now
    platforms: Dict[str, bool]
    metacritic: Optional[Dict[str, Any]] # score and url
    categories: List[Category]
    genres: List[Genre]
    screenshots: List[Screenshot]
    movies: List[Movie]
    recommendations: Recommendation
    achievements: Optional[Achievements]
    release_date: ReleaseDate
    support_info: SupportInfo
    background: str
    background_raw: str
    content_descriptors: ContentDescriptors
    ratings: Dict[str, Rating]

class AppDetailsResponse(TypedDict):
    success: bool
    data: AppDetailsData
