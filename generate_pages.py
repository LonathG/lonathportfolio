import csv
import re
import os

os.chdir(r"c:\Users\LONATH\Documents\Minds Studio\lonaths-portfolio")

with open('data/data.csv', 'r', encoding='utf-8') as f:
    projects = list(csv.DictReader(f))

def get_project_dict(p):
    return {
        'name': p.get('Name', ''),
        'slug': p.get('Slug', ''),
        'summary1': p.get('Project Summary', ''),
        'summary2': p.get('Project Summary 2', ''),
        'summary3': p.get('Project Summary 3', ''),
        'services': p.get('Services', ''),
        'year': p.get('Year', ''),
        'img_main': p.get('Main Image', ''),
        'img2': p.get('Second Image', ''),
        'img3': p.get('Third Image', ''),
        'img4': p.get('Fourth Image', ''),
        'img5': p.get('Fifth Image', ''),
        'img_featured': p.get('Featured Image', ''),
    }

def format_project_work(d):
    name = d['name']
    services = d['services']
    img = d['img_main']
    slug = d['slug']
    url = f"{slug}.html" if slug else "#"
    return f'''<div role="listitem" class="w-dyn-item">
                <div class="project-content">
                  <a href="{url}" class="project-wrapper-link w-inline-block"><img loading="lazy" src="{img}" alt="{name}" class="project-photo _01">
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

with open('detail_project.html', 'r', encoding='utf-8') as f:
    template_html = f.read()

for p in projects:
    d = get_project_dict(p)
    if not d['slug']:
        continue
    
    html = template_html
    name = d['name']
    
    # 1. Replace Title
    html = re.sub(r'<title>.*?</title>', f'<title>{name} | Lonath\'s Portfolio</title>', html, count=1)
    
    # 2. Big Title (H1)
    html = re.sub(
        r'(<h1[^>]*class="display-1 second )w-dyn-bind-empty("[^>]*>)</h1>',
        f'\\g<1>\\g<2>{name}</h1>',
        html
    )
    
    # 3. Project Summary 1
    html = re.sub(
        r'(<h2[^>]*class="display-1 second _1-7-rem smaller )w-dyn-bind-empty("[^>]*>)</h2>',
        f'\\g<1>\\g<2>{d["summary1"]}</h2>',
        html
    )
    
    # 4. Overview paragraph
    overview = d['summary2']
    if d['summary3']:
        overview += '<br><br>' + d['summary3']
        
    html = re.sub(
        r'(<p[^>]*class="display-1 second _1-7-rem smaller )w-dyn-bind-empty("[^>]*>)</p>',
        f'\\g<1>\\g<2>{overview}</p>',
        html
    )
    
    # 5. Client, Data, Service
    html = html.replace('<p class="subhead-main w-dyn-bind-empty"></p>', f'<p class="subhead-main">{name}</p>', 1)
    html = html.replace('<p class="subhead-main w-dyn-bind-empty"></p>', f'<p class="subhead-main">{d["year"]}</p>', 1)
    html = html.replace('<p class="subhead-main w-dyn-bind-empty"></p>', f'<p class="subhead-main">{d["services"]}</p>', 1)
    
    # 6. Images
    images = [img for img in [d['img2'], d['img3'], d['img4'], d['img5'], d['img_featured']] if img]
    if not images and d['img_main']:
        images = [d['img_main']]
        
    img_nodes = []
    for img in images:
        img_nodes.append(f'<div class="photo-wrapper"><img loading="eager" src="{img}" alt="{name}" class="work-photo-first"></div>')
        
    img_html = "\n            ".join(img_nodes)
    
    html = re.sub(
        r'(<div class="case-picture">).*?(</div>\s*</div>\s*</div>\s*</div>\s*</section>)',
        f'\\g<1>\n            {img_html}\n          \\g<2>',
        html,
        flags=re.DOTALL
    )
    
    # 7. Other projects
    other_projects_html = []
    for other_p in projects:
        other_d = get_project_dict(other_p)
        if other_d['slug'] and other_d['slug'] != d['slug']:
            other_projects_html.append(format_project_work(other_d))
    
    other_projects_str = "\n".join(other_projects_html)
    
    # Replace the exact wrapper in detail_project.html
    pattern_other = re.compile(r'<div role="list" class="project-grid w-dyn-items">.*?<div class="w-dyn-empty">\s*<div>No items found\.</div>\s*</div>', re.DOTALL)
    
    replacement_other = f'<div role="list" class="project-grid w-dyn-items">\n{other_projects_str}\n</div>'
    html = pattern_other.sub(replacement_other, html, 1)

    out_file = f"{d['slug']}.html"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {out_file}")

# Sequential link replacement in index.html
with open('index.html', 'r', encoding='utf-8') as f:
    text_index = f.read()

for p in projects:
    slug = p.get('Slug', '')
    url = f"{slug}.html" if slug else "#"
    text_index = text_index.replace('href="#" class="project-wrapper-link', f'href="{url}" class="project-wrapper-link', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text_index)
print("Updated index.html links")

# Sequential link replacement in work.html
with open('work.html', 'r', encoding='utf-8') as f:
    text_work = f.read()

for p in projects:
    slug = p.get('Slug', '')
    url = f"{slug}.html" if slug else "#"
    text_work = text_work.replace('href="#" class="project-wrapper-link', f'href="{url}" class="project-wrapper-link', 1)

with open('work.html', 'w', encoding='utf-8') as f:
    f.write(text_work)
print("Updated work.html links")
