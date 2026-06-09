import os
import sys

os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'
sys.path.insert(0, 'd:\\大数据专业综合课程设计\\travel_agent')

print("=== Testing Template Rendering ===")

# 测试1: 检查文件是否存在
template_path = "app/templates/index.html"
print(f"\n1. Checking template file: {template_path}")
print(f"   Exists: {os.path.exists(template_path)}")

# 测试2: 尝试读取模板文件
if os.path.exists(template_path):
    print("\n2. Reading template file...")
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"   File size: {len(content)} bytes")
        print(f"   First 100 chars: {content[:100]}")
else:
    print("   ERROR: Template file not found!")
    sys.exit(1)

# 测试3: 尝试渲染模板
print("\n3. Testing template rendering...")
try:
    from jinja2 import Environment, FileSystemLoader
    
    env = Environment(loader=FileSystemLoader("app/templates"))
    template = env.get_template("index.html")
    
    # 模拟FastAPI请求对象
    class MockRequest:
        def __init__(self):
            self.url = type('obj', (object,), {'path': '/'})()
    
    rendered = template.render(request=MockRequest())
    print(f"   Rendered successfully!")
    print(f"   Output size: {len(rendered)} bytes")
    
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test Complete ===")
