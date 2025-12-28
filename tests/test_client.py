import pytest
import httpx
from src.client import OpenRouterClient
from src.models import Message

FAKE_API_KEY = "sk-fake-key"
FAKE_MESSAGES = [Message(role="user", content="Hi")]
content = "Hello human!"


@pytest.mark.asyncio
async def test_send_messages_success(mocker):
    # Arrange
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message":
                    {
                        "content": content
                    }
            }
        ]
    }

    mock_httpx_client = mocker.AsyncMock()
    mock_httpx_client.post.return_value = mock_response

    mock_client_class = mocker.patch("httpx.AsyncClient")
    mock_client_class.return_value.__aenter__.return_value = mock_httpx_client

    client = OpenRouterClient(api_key=FAKE_API_KEY, model="test-model")

    # Act
    result = await client.send_messages(FAKE_MESSAGES)

    # Assert
    assert result == content

    mock_httpx_client.post.assert_called_once()
    called_url = mock_httpx_client.post.call_args[0][0]
    called_kwargs = mock_httpx_client.post.call_args[1]

    assert called_url == client.api_url
    assert called_kwargs["headers"]["Authorization"] == f"Bearer {FAKE_API_KEY}"


@pytest.mark.asyncio
async def test_send_messages_api_error(mocker):
    # Arrange
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=None, response=mock_response
    )

    mock_httpx_client = mocker.AsyncMock()
    mock_httpx_client.post.return_value = mock_response

    mocker.patch("httpx.AsyncClient").return_value.__aenter__.return_value = mock_httpx_client

    client = OpenRouterClient(api_key=FAKE_API_KEY, model="test-model")

    # Act
    result = await client.send_messages(FAKE_MESSAGES)

    # Assert
    assert "API Error 404" in result