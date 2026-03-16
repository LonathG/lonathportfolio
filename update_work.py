import csv
import re
import os

os.chdir(r"c:\Users\LONATH\Documents\Minds Studio\lonaths-portfolio")

with open('data/data.csv', 'r', encoding='utf-8') as f:
    projects = list(csv.DictReader(f))

print(f"Found {len(projects)} projects.")

def format_project_index(p):
    name = p.get('Name', '')
    services = p.get('Services', '')
    img = p.get('Main Image', '')
    return f'''<div role="listitem" class="collection-item w-dyn-item">
                <div class="project-content">
                  <a href="#" class="project-wrapper-link w-inline-block"><img loading="lazy" src="{img}" alt="{name}" class="project-photo _01">
                    <div class="left-part"></div>
                    <div class="right-part"></div>
                    <div class="top-part"></div>
                    <div class="bottom-part"></div>
                  </a>
                  <div class="margin-20px make-0px">
                    <div class="project-flex">
                      <div class="flex-pixel">
                        <h3 class="project-small-title biger">{name}</h3>
                        <h3 class="project-small-title biger">{name}</h3>
                      </div>
                      <div class="flex-pixel _2">
                        <h3 class="project-small-title lighter">{services}</h3>
                        <h3 class="project-small-title lighter">{services}</h3>
                      </div>
                    </div>
                  </div>
                </div>
              </div>'''

def format_project_work(p):
    name = p.get('Name', '')
    services = p.get('Services', '')
    img = p.get('Main Image', '')
    return f'''<div role="listitem" class="w-dyn-item">
                <div class="project-content">
                  <a href="#" class="project-wrapper-link w-inline-block"><img loading="lazy" src="{img}" alt="{name}" class="project-photo _01 smaller">
                    <div class="left-part"></div>
                    <div class="right-part"></div>
                    <div class="top-part"></div>
                    <div class="bottom-part"></div>
                  </a>
                  <div class="margin-20px make-0px">
                    <div class="project-flex">
                      <div class="flex-pixel">
                        <h3 class="project-small-title biger">{name}</h3>
                        <h3 class="project-small-title biger">{name}</h3>
                      </div>
                      <div class="flex-pixel _2">
                        <h3 class="project-small-title lighter">{services}</h3>
                        <h3 class="project-small-title lighter">{services}</h3>
                      </div>
                    </div>
                  </div>
                </div>
              </div>'''

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

pattern_index = re.compile(r'<div role="list" class="w-dyn-items">.*?<div class="w-dyn-empty">\s*<div>No items found\.</div>\s*</div>', re.DOTALL)
matches = pattern_index.findall(index_html)
print(f"Found {len(matches)} w-dyn-items in index.html.")

new_index_html = index_html
for i, match in enumerate(matches):
    if i < len(projects):
        replacement = f'<div role="list" class="w-dyn-items">\n{format_project_index(projects[i])}\n</div>'
        new_index_html = new_index_html.replace(match, replacement, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_index_html)

with open('work.html', 'r', encoding='utf-8') as f:
    work_html = f.read()

pattern_work = re.compile(r'<div role="list" class="project-grid w-dyn-items">.*?<div class="w-dyn-empty">\s*<div>No items found\.</div>\s*</div>', re.DOTALL)
matches_work = pattern_work.findall(work_html)
print(f"Found {len(matches_work)} project-grid w-dyn-items in work.html.")

if matches_work:
    items_html = "\\n".join([format_project_work(p) for p in projects])
    replacement_work = f'<div role="list" class="project-grid w-dyn-items">\n{items_html}\n</div>'
    new_work_html = work_html.replace(matches_work[0], replacement_work, 1)
    with open('work.html', 'w', encoding='utf-8') as f:
        f.write(new_work_html)

print("Done replacing.")
