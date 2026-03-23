from openai import AsyncOpenAI

client = AsyncOpenAI()

async def stream_final_analysis(event, log_features, intel, history, risk):

    stream = await client.responses.create(
        model="gpt-4.1",
        input=f"""
Event: {event.event}
Logs: {log_features.model_dump()}
Intel: {intel.model_dump()}
History: {history.model_dump()}
Risk: {risk.model_dump()}

Explain the threat and give recommended actions.
""",
        stream=True
    )

    async for chunk in stream:
        if chunk.type == "response.output_text.delta":
            yield chunk.delta
