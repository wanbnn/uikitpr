import json

import pytest
from pyreact.server import render_to_static_markup

from uikitpr import (
    MOTION_FINISH,
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
    spring_keyframes,
    stagger,
)


def test_motion_serializes_preset_triggers_and_interactions():
    node = Motion(
        "Conteúdo",
        preset="fade-up",
        trigger="in-view",
        while_hover={"transform": "scale(1.04)"},
        transition=Transition(duration=0.6, delay=0.1),
        motion_id="hero",
    )
    config = json.loads(node.props["data-uipr-motion"])
    assert node.props["data-uipr-motion-id"] == "hero"
    assert config["preset"] == "fade-up"
    assert config["trigger"] == "in-view"
    assert config["whileHover"]["transform"] == "scale(1.04)"
    assert config["transition"]["duration"] == 600
    assert config["transition"]["delay"] == 100


def test_spring_keyframes_are_deterministic_and_validate_physics():
    frames = spring_keyframes(spring=Spring(stiffness=190, damping=18), frames=40)
    assert len(frames) == 40
    assert frames[0] == 0
    assert frames[-1] == 1
    assert any(value > 1 for value in frames)
    with pytest.raises(ValueError):
        spring_keyframes(spring=Spring(mass=0))


def test_stagger_wraps_items_with_incremental_delays():
    nodes = stagger(["a", "b", "c"], each=0.12, delay=0.05)
    delays = [
        json.loads(node.props["data-uipr-motion"])["transition"]["delay"]
        for node in nodes
    ]
    assert delays == [50, 170, 290]


def test_group_and_timeline_are_serialized():
    group = MotionGroup("item", preset="scale", stagger=0.1)
    group_config = json.loads(group.props["data-uipr-motion-group"])
    assert group_config["stagger"] == 100

    timeline = Timeline(
        id="intro",
        steps=[
            TimelineStep(
                "hero",
                "fade-up",
                transition=Transition(duration=0.3),
            )
        ],
    )
    node = MotionTimeline("conteúdo", timeline=timeline)
    config = json.loads(node.props["data-uipr-timeline"])
    assert config["id"] == "intro"
    assert config["steps"][0]["transition"]["duration"] == 300


def test_runtime_and_event_helpers():
    html = render_to_static_markup(MotionRuntime())
    assert 'data-uipr-motion-runtime="true"' in html
    assert "data:text/javascript;base64," in html
    assert "window.UIKitPRMotion" in motion_script()
    assert motion_event(MOTION_FINISH, {"id": "card"}) == {
        "name": "uipr:motion:finish",
        "detail": {"id": "card"},
    }
    assert len(motion_script(minified=True)) < len(motion_script())
    assert not motion_script(minified=True).lstrip().startswith("//")


def test_declarative_motion_control():
    props = motion_control(
        "hero card",
        "shake",
        transition=Transition(duration=0.62),
    )
    config = json.loads(props["data-uipr-motion-control"])
    assert config == {
        "target": "hero card",
        "preset": "shake",
        "transition": {
            "duration": 620,
            "delay": 0,
            "easing": "cubic-bezier(0.22, 1, 0.36, 1)",
            "repeat": 0,
            "direction": "normal",
            "fill": "both",
        },
    }
    assert "data-uipr-motion-control" in motion_script()
    with pytest.raises(ValueError):
        motion_control("", "pop")
