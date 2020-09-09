import pytest
from slack_sdk.models.blocks import PlainTextObject, DividerBlock
from slack_sdk.models.views import View

from slack_bolt import BoltResponse
from slack_bolt.context.ack.async_ack import AsyncAck


class TestAsyncAsyncAck:
    @pytest.mark.asyncio
    async def test_text(self):
        ack = AsyncAck()
        response: BoltResponse = await ack(text="foo")
        assert (response.status, response.body) == (200, "foo")

    @pytest.mark.asyncio
    async def test_blocks(self):
        ack = AsyncAck()
        response: BoltResponse = await ack(text="foo", blocks=[{"type": "divider"}])
        assert (response.status, response.body) == (
            200,
            '{"text": "foo", "blocks": [{"type": "divider"}]}',
        )

    @pytest.mark.asyncio
    async def test_response_type(self):
        ack = AsyncAck()
        response: BoltResponse = await ack(text="foo", response_type="in_channel")
        assert (response.status, response.body) == (
            200,
            '{"text": "foo", "response_type": "in_channel"}',
        )

    @pytest.mark.asyncio
    async def test_view_errors(self):
        ack = AsyncAck()
        response: BoltResponse = await ack(
            response_action="errors",
            errors={
                "block_title": "Title is required",
                "block_description": "Description must be longer than 10 characters",
            },
        )
        assert (response.status, response.body) == (
            200,
            '{"response_action": "errors", '
            '"errors": {'
            '"block_title": "Title is required", '
            '"block_description": "Description must be longer than 10 characters"'
            "}"
            "}",
        )

    @pytest.mark.asyncio
    async def test_view_update(self):
        ack = AsyncAck()
        response: BoltResponse = await ack(
            response_action="update",
            view={
                "type": "modal",
                "callbAsyncAck_id": "view-id",
                "title": {"type": "plain_text", "text": "My App",},
                "close": {"type": "plain_text", "text": "Cancel",},
                "blocks": [{"type": "divider", "block_id": "b"}],
            },
        )
        assert (response.status, response.body) == (
            200,
            '{"response_action": "update", '
            '"view": {'
            '"type": "modal", '
            '"callbAsyncAck_id": "view-id", '
            '"title": {"type": "plain_text", "text": "My App"}, '
            '"close": {"type": "plain_text", "text": "Cancel"}, '
            '"blocks": [{"type": "divider", "block_id": "b"}]'
            "}"
            "}",
        )

    @pytest.mark.asyncio
    async def test_view_update_2(self):
        ack = AsyncAck()
        response: BoltResponse = await ack(
            response_action="update",
            view=View(
                type="modal",
                callback_id="view-id",
                title=PlainTextObject(text="My App"),
                close=PlainTextObject(text="Cancel"),
                blocks=[DividerBlock(block_id="b")],
            ),
        )
        assert (response.status, response.body) == (
            200,
            ""
            '{"response_action": "update", '
            '"view": {'
            '"blocks": [{"block_id": "b", "type": "divider"}], '
            '"callback_id": "view-id", '
            '"close": {"text": "Cancel", "type": "plain_text"}, '
            '"title": {"text": "My App", "type": "plain_text"}, '
            '"type": "modal"'
            "}"
            "}",
        )