from flask import Flask, render_template_string
import asyncio
from subxtpy import SubxtClient

app = Flask(__name__)

# Asynchronous function to get the latest block information
async def get_latest_block_info():
    client = await SubxtClient.from_url("wss://rpc.polkadot.io:443")

    # Subscribe to new blocks and get the latest block
    subscription = await client.subscribe_new_blocks()
    block = await subscription.__anext__()

    block_number = block['block_number']
    block_hash = block['block_hash']
    extrinsics = block['extrinsics']

    return {
        'block_number': block_number,
        'block_hash': block_hash,
        'extrinsics': extrinsics
    }

@app.route('/')
def index():
    # Run the asynchronous function in the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    block_info = loop.run_until_complete(get_latest_block_info())

    # Render the block information in an HTML template
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Subxtpy Flask Integration</title>
    </head>
    <body>
        <h1>Latest Block Information</h1>
        <p><strong>Block Number:</strong> {{ block_number }}</p>
        <p><strong>Block Hash:</strong> {{ block_hash }}</p>
        <h2>Extrinsics</h2>
        <ul>
        {% for extrinsic in extrinsics %}
            <li>
                <strong>Pallet:</strong> {{ extrinsic['pallet'] }},
                <strong>Call:</strong> {{ extrinsic['call'] }}
            </li>
        {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(template, **block_info)

if __name__ == '__main__':
    app.run(debug=True)