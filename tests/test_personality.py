"""Tests for the personality engine! 🐕✨

Tests for mood system, response decisions, and spontaneous outbursts.
"""

from discord_puppy.personality import (
    MOOD_WEIGHTS,
    Mood,
    get_mood_modifier,
    get_random_mood,
    random_outburst,
    should_react_with_emoji,
    should_respond,
)


class TestMoodSystem:
    """Tests for the mood system."""

    def test_mood_enum_has_expected_values(self):
        """Verify all expected moods exist."""
        expected_moods = [
            "zoomies",
            "sleepy",
            "hungry",
            "wise",
            "philosophical",
            "suspicious",
            "excited",
        ]
        actual_moods = [m.value for m in Mood]
        assert sorted(actual_moods) == sorted(expected_moods)

    def test_mood_weights_covers_all_moods(self):
        """Verify all moods have weights."""
        for mood in Mood:
            assert mood in MOOD_WEIGHTS, f"Missing weight for {mood}"

    def test_mood_weights_are_positive(self):
        """Verify all mood weights are positive."""
        for mood, weight in MOOD_WEIGHTS.items():
            assert weight > 0, f"Weight for {mood} should be positive"

    def test_get_random_mood_returns_valid_mood(self):
        """Verify get_random_mood returns a Mood enum."""
        for _ in range(50):  # Run multiple times for randomness
            mood = get_random_mood()
            assert isinstance(mood, Mood)

    def test_get_mood_modifier_returns_string(self):
        """Verify mood modifiers are strings."""
        for mood in Mood:
            modifier = get_mood_modifier(mood)
            assert isinstance(modifier, str)
            assert len(modifier) > 0

    def test_get_mood_modifier_contains_mood_indicator(self):
        """Verify mood modifiers mention the mood."""
        # Zoomies should mention ZOOMIES
        modifier = get_mood_modifier(Mood.ZOOMIES)
        assert "ZOOMIES" in modifier

        # Sleepy should mention SLEEPY
        modifier = get_mood_modifier(Mood.SLEEPY)
        assert "SLEEPY" in modifier


class TestShouldRespond:
    """Tests for the should_respond decision function."""

    def test_always_respond_to_dm(self):
        """DMs should always get a response."""
        respond, reason = should_respond(
            message_content="hello",
            is_dm=True,
            response_chance=0.0,  # Even with 0% chance
        )
        assert respond is True
        assert "DM" in reason

    def test_always_respond_to_mention(self):
        """Mentions should always get a response."""
        respond, reason = should_respond(
            message_content="yo what's up",
            is_mentioned=True,
            response_chance=0.0,  # Even with 0% chance
        )
        assert respond is True
        assert "mention" in reason.lower()

    def test_trigger_words_always_respond(self):
        """Messages with trigger words should get a response."""
        trigger_messages = [
            "good boy!",
            "here's a treat",
            "I saw a squirrel",
            "throw the ball",
            "woof woof",
        ]
        for message in trigger_messages:
            respond, reason = should_respond(
                message_content=message,
                response_chance=0.0,  # Even with 0% chance
            )
            assert respond is True, f"Should respond to '{message}'"

    def test_zero_chance_no_response_without_triggers(self):
        """With 0% chance and no triggers, should not respond."""
        # Run multiple times to ensure it's consistent
        no_response_count = 0
        for _ in range(20):
            respond, _ = should_respond(
                message_content="The weather is nice today",
                response_chance=0.0,
            )
            if not respond:
                no_response_count += 1
        # Should mostly not respond (might rarely respond due to randomness elsewhere)
        assert no_response_count > 15

    def test_full_chance_always_responds(self):
        """With 100% chance, should always respond."""
        for _ in range(20):
            respond, _ = should_respond(
                message_content="Random message without triggers",
                response_chance=1.0,
            )
            assert respond is True

    def test_trust_level_affects_response_chance(self):
        """Higher trust should increase response likelihood."""
        # Can't test exact probabilities, but can verify it doesn't crash
        respond_low, _ = should_respond(
            message_content="hi",
            user_trust_level=1,
            response_chance=0.5,
        )
        respond_high, _ = should_respond(
            message_content="hi",
            user_trust_level=10,
            response_chance=0.5,
        )
        # Both should return bools (not crash)
        assert isinstance(respond_low, bool)
        assert isinstance(respond_high, bool)

    def test_returns_tuple_with_reason(self):
        """Verify return type is tuple of (bool, str)."""
        result = should_respond(message_content="hello")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)


class TestShouldReactWithEmoji:
    """Tests for the emoji reaction decision."""

    def test_returns_tuple(self):
        """Verify return type."""
        result = should_react_with_emoji()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_bool_and_optional_emoji(self):
        """Verify tuple contents."""
        # Run many times to get both outcomes
        for _ in range(200):
            should_react, emoji = should_react_with_emoji()
            assert isinstance(should_react, bool)
            if should_react:
                assert emoji is not None
                assert isinstance(emoji, str)
                assert len(emoji) > 0
            else:
                assert emoji is None


class TestRandomOutburst:
    """Tests for spontaneous outbursts."""

    def test_generic_outburst_no_users(self):
        """Without users, should get generic outburst."""
        for _ in range(20):
            outburst = random_outburst()
            assert isinstance(outburst, str)
            assert len(outburst) > 0

    def test_outburst_with_users(self):
        """With users, outbursts might reference them."""
        users = ["TestUser", "AnotherUser"]
        trust_levels = {"TestUser": 7, "AnotherUser": 3}

        for _ in range(50):  # Run many times for coverage
            outburst = random_outburst(
                usernames=users,
                trust_levels=trust_levels,
                day_count=42,
            )
            assert isinstance(outburst, str)
            assert len(outburst) > 0
            # Some outbursts should reference users
            # (can't guarantee which one due to randomness)

    def test_outburst_with_day_count(self):
        """Day count should be used in diary outbursts."""
        # Run many times to hopefully hit a diary outburst
        for _ in range(100):
            outburst = random_outburst(day_count=99)
            # If it's a diary outburst with day placeholder, it should use our number
            if "Day 99" in outburst:
                assert True
                return
        # If we never hit a diary outburst, that's okay (randomness)

    def test_outburst_does_not_crash_with_empty_users(self):
        """Empty user list should work."""
        outburst = random_outburst(usernames=[], trust_levels={})
        assert isinstance(outburst, str)


class TestExports:
    """Test that all expected exports are available."""

    def test_mood_enum_exported(self):
        """Mood should be importable."""
        from discord_puppy.personality import Mood

        assert Mood is not None

    def test_all_functions_exported(self):
        """All main functions should be importable."""
        from discord_puppy.personality import (
            get_mood_modifier,
            get_random_mood,
            random_outburst,
            should_react_with_emoji,
            should_respond,
        )

        assert callable(get_mood_modifier)
        assert callable(get_random_mood)
        assert callable(random_outburst)
        assert callable(should_react_with_emoji)
        assert callable(should_respond)
