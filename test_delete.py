import asyncio
import aiosqlite

async def test_delete():
    db = await aiosqlite.connect("travel_assistant.db")
    db.row_factory = aiosqlite.Row
    
    # 检查删除前的记录数
    cursor = await db.execute("SELECT COUNT(*) as count FROM conversations")
    row = await cursor.fetchone()
    print(f"删除前记录数: {row['count']}")
    
    # 执行删除
    await db.execute("DELETE FROM conversations")
    await db.commit()
    
    # 检查删除后的记录数
    cursor = await db.execute("SELECT COUNT(*) as count FROM conversations")
    row = await cursor.fetchone()
    print(f"删除后记录数: {row['count']}")
    
    await db.close()
    print("操作完成")

asyncio.run(test_delete())