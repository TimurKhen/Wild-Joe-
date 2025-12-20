import asyncio

import test_user_1
import test_user_2

asyncio.gather(
    test_user_1.run(),
    test_user_2.run(),
)
