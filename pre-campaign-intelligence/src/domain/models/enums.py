from enum import StrEnum


class CampaignGoal(StrEnum):
    BRAND_AWARENESS = "brand awareness"
    BUILDING_ENGAGEMENT = "building engagement"
    AUTHENTIC_CONTENT = "authentic content"


class PromotingItem(StrEnum):
    PHYSICAL_PRODUCT = "physical product"
    ONLINE_SERVICE = "online service"
    IN_STORE_EXPERIENCE = "in-store experience"


class VideoOrientation(StrEnum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    SQUARE = "square"


class VideoType(StrEnum):
    BEFORE_AFTER = "before/after"
    INFORMATION = "information"
    LIFESTYLE = "lifestyle"
    REVIEWS = "reviews"
    PRODUCT_DEMO = "product demo"
    RECIPES = "recipes"
    TESTIMONIALS = "testimonials"
    TUTORIALS = "tutorials"
    UNBOXING = "unboxing"