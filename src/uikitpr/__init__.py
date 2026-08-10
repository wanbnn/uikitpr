"""UIKitPR — framework visual utility-first para PyReact."""

from .cache import (
    CachedAsset,
    CacheManager,
    CachePolicy,
    CacheRuntime,
    cache_script,
)
from .components import (
    Alert,
    Avatar,
    Badge,
    Box,
    Breadcrumb,
    Button,
    Card,
    CardBody,
    CardFooter,
    CardHeader,
    Checkbox,
    Container,
    Divider,
    Grid,
    Heading,
    IconButton,
    Input,
    Modal,
    Navbar,
    NavbarBrand,
    NavbarContent,
    Progress,
    Select,
    Spinner,
    Stack,
    Switch,
    Table,
    TableContainer,
    Text,
    Textarea,
)
from .core import cx, utility
from .effects import (
    AnimatedText,
    AuroraBackground,
    BeamBackground,
    BlurText,
    DotBackground,
    GradientText,
    GridBackground,
    Marquee,
    ShinyText,
    SplitText,
    SpotlightCard,
    StarBorder,
)
from .loaders import (
    BarsLoader,
    DotsLoader,
    OrbitLoader,
    PageLoader,
    PulseLoader,
    RingLoader,
    Skeleton,
    SkeletonCard,
    WaveLoader,
)
from .motion import (
    MOTION_CANCEL,
    MOTION_FINISH,
    MOTION_START,
    MOTION_UPDATE,
    PRESETS,
    Motion,
    MotionGroup,
    MotionRuntime,
    MotionTimeline,
    Spring,
    Timeline,
    TimelineStep,
    Transition,
    motion_event,
    motion_control,
    motion_script,
    motion_script_data_url,
    spring_keyframes,
    stagger,
)
from .theme import (
    Styles,
    Theme,
    UIProvider,
    create_theme,
    stylesheet,
    stylesheet_data_url,
)
from . import creative
from .creative import (
    ANIMATIONS as CREATIVE_ANIMATIONS,
    BACKGROUNDS as CREATIVE_BACKGROUNDS,
    CREATIVE_CATALOG,
    TEXT_ANIMATIONS as CREATIVE_TEXT_ANIMATIONS,
    UI_COMPONENTS as CREATIVE_UI_COMPONENTS,
    Creative,
    CreativeRuntime,
    creative_script,
)

for _creative_name in (*CREATIVE_TEXT_ANIMATIONS, *CREATIVE_ANIMATIONS, *CREATIVE_UI_COMPONENTS, *CREATIVE_BACKGROUNDS):
    if _creative_name not in globals():
        globals()[_creative_name] = getattr(creative, _creative_name)

# ``Stack`` is already UIKitPR's foundational layout primitive.
CreativeStack = creative.Stack

__version__ = "0.3.2"

__all__ = [
    "Alert", "AnimatedText", "AuroraBackground", "Avatar", "Badge",
    "BarsLoader", "BeamBackground", "BlurText", "Box", "Breadcrumb", "Button",
    "CacheManager", "CachePolicy", "CacheRuntime", "CachedAsset", "Card",
    "CardBody", "CardFooter", "CardHeader", "Checkbox", "Container",
    "Divider", "DotBackground", "DotsLoader", "GradientText", "Grid",
    "GridBackground", "Heading", "IconButton", "Input", "Marquee", "Modal",
    "MOTION_CANCEL", "MOTION_FINISH", "MOTION_START", "MOTION_UPDATE", "Motion",
    "MotionGroup", "MotionRuntime", "MotionTimeline", "Navbar",
    "NavbarBrand", "NavbarContent", "Progress", "Select", "Spinner", "Stack",
    "ShinyText", "SplitText", "SpotlightCard", "StarBorder", "Styles", "Switch",
    "Table", "TableContainer", "Text", "Textarea", "Theme",
    "Transition", "Timeline", "TimelineStep", "Spring", "PRESETS", "OrbitLoader",
    "PageLoader", "PulseLoader", "RingLoader", "Skeleton", "SkeletonCard",
    "UIProvider", "WaveLoader", "cache_script", "create_theme", "cx",
    "motion_control", "motion_event",
    "motion_script", "motion_script_data_url", "spring_keyframes", "stagger",
    "stylesheet", "stylesheet_data_url", "utility",
    "CREATIVE_ANIMATIONS", "CREATIVE_BACKGROUNDS", "CREATIVE_TEXT_ANIMATIONS",
    "CREATIVE_UI_COMPONENTS", "CreativeStack", "CREATIVE_CATALOG", "Creative",
    "CreativeRuntime", "creative", "creative_script",
]

__all__.extend(
    name
    for name in (*CREATIVE_TEXT_ANIMATIONS, *CREATIVE_ANIMATIONS, *CREATIVE_UI_COMPONENTS, *CREATIVE_BACKGROUNDS)
    if name not in __all__ and name != "Stack"
)
