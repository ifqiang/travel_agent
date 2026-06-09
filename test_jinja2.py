import sys
import os

os.chdir('d:\\大数据专业综合课程设计\\travel_agent')
os.environ['PYTHONPATH'] = 'd:\\大数据专业综合课程设计\\travel_agent'

print("=== Testing Jinja2 Template Rendering ===")

try:
    from jinja2 import Environment, FileSystemLoader
    
    # 创建Jinja2环境
    template_dir = "app/templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # 测试简单模板
    print("Testing test.html...")
    template = env.get_template("test.html")
    result = template.render()
    print("SUCCESS: test.html rendered!")
    print("Content:", result[:200])
    
    # 测试index.html
    print("\nTesting index.html...")
    template = env.get_template("index.html")
    result = template.render()
    print("SUCCESS: index.html rendered!")
    print("Content length:", len(result))
    
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()