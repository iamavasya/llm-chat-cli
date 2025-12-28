import pytest
from unittest.mock import AsyncMock
from src.services import ChatService
from src.models import Message

@pytest.fixture
def mock_client():
    client = AsyncMock()
    return client

@pytest.fixture
def service(mock_client):
    return ChatService(mock_client)

@pytest.mark.asyncio
async def test_ask_adds_messages_to_history(service, mock_client):
    # Arrange
    user_text = "Hello"
    expected_response = "Hi there!"

    mock_client.send_messages.return_value = expected_response

    # Act
    result = await service.ask(user_text)

    # Assert
    assert result == expected_response

    assert len(service._history) == 3
    assert service._history[1].role == "user"
    assert service._history[1].content == user_text
    assert service._history[2].role == "assistant"
    assert service._history[2].content == expected_response


@pytest.mark.asyncio
async def test_client_is_called_with_correct_history(service, mock_client):
    # Arrange
    user_text = "Why?"
    mock_client.send_messages.return_value = "Because I said so!"

    # Act
    await service.ask(user_text)

    # Assert
    mock_client.send_messages.assert_called_once()

    passed_history = mock_client.send_messages.call_args[0][0]

    assert isinstance(passed_history, list)

    user_message = passed_history[-2]

    assert user_message.role == "user"
    assert user_message.content == user_text