from uikitpr import cx, utility


def test_cx_combines_nested_and_conditional_classes():
    assert cx("flex gap-2", {"hidden": False, "items-center": True}, ["p-4", None]) == (
        "flex gap-2 items-center p-4"
    )


def test_cx_removes_duplicates_and_utility_is_alias():
    assert utility("flex", "flex", ["gap-4"]) == "flex gap-4"

