#!/usr/bin/env python3
"""Rebuild full-length note pages from archived sources, replacing note figures with prose."""
from pathlib import Path
import json
import re
import base64
import zipfile
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / '_source_archive' / 'github_zip'
MATH = ARCHIVE / 'Math-s-interesting-things-main'
STATS = ARCHIVE / 'stat.pre-main'
PAGES = ROOT / '_pages'
ZIP = Path('/Users/luyu/Desktop/github.zip')
MEDIA = ROOT / 'assets' / 'img'

MATH_PAGES = [
    ('Mathematical Analysis 1.qmd', 'Analysis 1', 'analysis-1'),
    ('Calculus.qmd', 'Calculus', 'calculus'),
    ('mth107.qmd', 'Advanced Linear Algebra', 'linear-algebra'),
    ('mth1113.qmd', 'Prob. and Stat.', 'probability-statistics'),
    ('stat_learn.qmd', 'Statistical Learning', 'statistical-learning'),
]
STAT_PAGES = [
    ('2024surf.qmd', '2024 SURF', '2024-surf', True),
    ('SurveySampling.qmd', 'Survey Sampling', 'survey-sampling', True),
    ('MTH203Project.qmd', 'MIP Algorithm Development', 'mip-algorithm', True),
    ('distribution transformation.qmd', 'Mathematical Statistics', 'mathematical-statistics', False),
    ('survival_analysis.qmd', 'Survival Analysis', 'survival-analysis', False),
    ('resampling.qmd', 'Resampling', 'resampling', False),
    ('Linear Models and Regression Analysis/glm pre.qmd', 'Generalized Linear Models', 'generalized-linear-models', False),
    ('Linear Models and Regression Analysis/some tips about stats.qmd', 'Statistics Tips', 'statistics-tips', False),
    ('nothing.qmd', 'Additional Statistics Notes', 'additional-notes', False),
]

# Descriptions for screenshots whose meaning would otherwise be lost.
FIGURES = {
    '2024surf.qmd': {
        'f1.jpg': 'The cohort moves from 450 records to 319 complete records after 131 exclusions; Cox-Lasso and backward Cox selection are then compared.',
        'f2.jpg': 'The chart compares observed survival outcomes across the pesticide groups described above.',
        'f3.jpg': 'The coefficient display summarizes variables retained by the penalized Cox model.',
    },
    'Mathematical Analysis 1.qmd': {
        'clipboard-120870201.png': 'The first sketch motivates a limit argument through a geometric example before introducing formal notation.',
        'clipboard-37991470.png': 'The second sketch compares the same intuitive picture with the symbolic steps of the argument.',
        'clipboard-1727062441.png': 'If a continuous function is positive at one point, nearby values remain positive.',
        'clipboard-1707466155.png': 'A sufficiently small neighborhood around the point keeps the continuous function above zero.',
        'clipboard-317793846.png': 'Complex numbers lack an order compatible with field operations, so their norm supplies a useful notion of size.',
        'clipboard-4061595181.png': 'An infinite subset of the natural numbers can be listed in increasing order, establishing countable infinity.',
        'clipboard-4280451848.png': 'The supremum proof tests values below and above the proposed least upper bound to rule both out.',
        'clipboard-743581739.png': 'Nested intervals give a construction of the supremum from successively tighter bounds.',
        'clipboard-899547799.png': 'The upper-bound construction narrows the possible location of a unique supremum.',
        'clipboard-3519769833.png': 'The rational numbers below the square root of two show why the rational field is not complete.',
        'clipboard-1103791551.png': 'Each nested interval meets the set, so its limiting endpoint approaches the set supremum.',
        'clipboard-4085119236.png': 'The finite-covering argument selects a subinterval inside one open set and derives a contradiction.',
        'clipboard-3097473254.png': 'The lecture proof emphasizes that every inference needs a stated reason.',
        'clipboard-3258860968.png': 'Cantor diagonalization constructs a subset of the natural numbers missing from any proposed enumeration.',
        'clipboard-1883408292.png': 'A bijection pairs elements of two sets so that each has exactly one partner.',
        'clipboard-819524834.png': 'The companion example checks whether the proposed correspondence is one-to-one and onto.',
        'clipboard-1556053307.png': 'In a continuity argument, choose the smaller of two candidate delta values so both requirements hold.',
        'clipboard-597490383.png': 'The second continuity example again uses a common delta that satisfies every local bound.',
        'clipboard-3326791247.png': 'A sequence chosen near a supremum approaches it while continuity transfers the limiting value.',
    },
    'stat_learn.qmd': {
        '5c1925776904a7003b6430952f71eb71.jpg': 'For a normal sample, orthogonal components of the data vector separate the sample mean from residual variation.',
        'clipboard-3590925628.png': 'A prior concentrated near zero discourages large regression coefficients, giving the Bayesian view of regularization.',
        'clipboard-4201197806.png': 'At a constrained optimum, the gradient of the loss balances the gradient associated with the penalty.',
        'clipboard-3731736673.png': 'The corners of an L1 constraint make zero coefficients more likely when a loss contour touches the feasible region.',
    },
    'mth1113.qmd': {
        'clipboard-2219722049.png': 'A hypothesis test compares an observed statistic with its null reference distribution and a chosen rejection region.',
        'clipboard-3291557304.png': 'The unpaired two-sample t procedure combines within-group variation through the pooled standard deviation.',
        'clipboard-2348163751.png': 'The R output arranges several exploratory plots, including grouped summaries and a regression display, for comparison.',
        'clipboard-2819513011.png': 'Estimating the population variance from a sample uses n minus one degrees of freedom after estimating the sample mean.',
        'clipboard-1774849890.png': 'Paired quantitative observations can be plotted to reveal the direction and strength of their association.',
        'clipboard-807464638.png': 'A fitted regression line summarizes the average linear pattern while individual points retain their variation.',
        'clipboard-3333660003.png': 'Regression to the mean describes how unusually high or low measurements tend to be less extreme on a later measurement.',
        'clipboard-1881050695.png': 'Predicting far outside the observed range is unstable because the fitted pattern has not been checked there.',
        'clipboard-2419630434.png': 'A residual plot without a systematic pattern is more consistent with a linear mean model.',
        'clipboard-3592387892.png': 'A curved or widening residual pattern signals that the linear model or constant-variance assumption may be inadequate.',
        'clipboard-2849357671.png': 'A long distribution tail pulls the mean farther than the median, so an outlier can change the mean substantially.',
        'clipboard-2111278063.png': 'Quartile spacing helps distinguish left skew, right skew, and a roughly symmetric distribution.',
        'clipboard-2144359450.png': 'Intervals measured in standard deviations summarize the spread around a mean.',
        'clipboard-1854557292.png': 'The distribution sketches compare how much mass lies near or far from the mean.',
        'clipboard-3026116502.png': 'The dot plot compares graduation rates for all athletes with basketball players.',
        'clipboard-858121668.png': 'A designed experiment assigns treatments and compares responses to support causal questions.',
        'clipboard-206208503.png': 'A joint probability table sums across the other variable to obtain a marginal distribution.',
        'clipboard-369824916.png': 'For a function of two random variables, expectation weights each possible input pair by its joint probability.',
        'clipboard-1910128728.png': 'For a continuous variable, probabilities are areas under a density curve rather than heights at single points.',
        'clipboard-4061434485.png': 'Covariance records whether two variables tend to move in the same or opposite directions.',
        'clipboard-2808960987.png': 'Positive, negative, or near-zero covariance corresponds to different patterns of joint variation.',
        'clipboard-804415.png': 'A very small binomial tail probability marks an observed number of successes as unusual under the assumed model.',
        'clipboard-1400086523.png': 'A normal quantile plot compares ordered observations with expected normal quantiles to check the distributional shape.',
        'clipboard-2929822579.png': 'Paired observations support studying correlation and regression, unlike a comparison of two unrelated sample means.',
        'clipboard-1345728232.png': 'The closing course image accompanies the reflection on learning statistics beyond an exam.',
    },
    'distribution transformation.qmd': {
        'clipboard-1538267932.png': 'The explanatory-variable space provides the subspace onto which regression projects the response.',
    },
    'mth106.qmd': {
        'clipboard-2874869730.png': 'Orthogonality isolates the constant Fourier coefficient by integrating against 1 over a full period.',
        'clipboard-2116251045.png': 'Integrating against a cosine basis function isolates the corresponding cosine coefficient.',
        'clipboard-3831873794.png': 'Integrating against a sine basis function isolates the corresponding sine coefficient.',
        'clipboard-935811087.png': 'An initial-value problem combines a differential equation with the values prescribed at the initial point.',
        'clipboard-381625365.png': 'Existence asks whether a solution curve passes through the initial value; uniqueness asks whether more than one can do so.',
        'clipboard-1219784406.png': 'The phase line for the logistic equation marks the equilibria and the direction of change between them.',
        'clipboard-1811387429.png': 'A solution curve follows the direction field determined by the autonomous equation.',
        'clipboard-1854338105.png': 'A horizontal shift of an autonomous-equation solution is another solution because the equation has no explicit time dependence.',
        'clipboard-2402865730.png': 'The integral form of a separable equation expresses the solution through accumulated change.',
        'clipboard-1563205732.png': 'The worked separable-equation example applies the initial value after integration.',
        'clipboard-960467589.png': 'The integrating-factor solution uses the initial condition to determine its integration constant.',
        'clipboard-2824072994.png': 'The diagram tracks the error between an exact solution and its approximation.',
        'clipboard-4209968738.png': 'The companion diagram compares the approximation with the solution over the interval.',
    },
    'mth107.qmd': {
        'clipboard-3621424598.png': 'The least-squares picture projects the response onto the column space of the design matrix.',
        'clipboard-289964766.png': 'The residual is orthogonal to the fitted projection in the least-squares example.',
        'clipboard-2928221853.png': 'The diagram illustrates addition of subspaces and how their vectors combine.',
        'clipboard-654847461.png': 'The example contrasts a unique direct-sum decomposition with a non-unique sum.',
        'clipboard-868461290.png': 'The lemma diagram follows how a linear map acts on sums of vectors.',
        'clipboard-3941908751.png': 'The companion diagram follows scalar multiplication through the linear map.',
        'clipboard-41621451.png': 'Projection selects the component inside the chosen approximation space.',
        'clipboard-3096739023.png': 'Subtracting the projection leaves an error component orthogonal to that space.',
        'clipboard-703567150.png': 'The function-space example uses projection to approximate a function with simpler basis functions.',
        'clipboard-3068495766.png': 'The tutorial problem asks for an example or counterexample to test the stated mapping property.',
        'clipboard-1407097711.png': 'The example checks both compositions to decide whether the maps are inverses.',
    },
    'Calculus.qmd': {
        'surface-3%20cylinder.jpg': 'The boundary of three intersecting cylinders is divided into symmetric surface pieces.',
        's3.jpg': 'Symmetry reduces the surface-area calculation to one representative curved patch.',
        "method1's%20photo%20behind.png": 'The first volume method separates a central region from six symmetric outer pieces.',
        'm3.jpg': 'Cross-sections change shape at the threshold shown in the integral limits.',
        '3%20cylinders%20method%202.jpg': 'The alternative method decomposes the three-cylinder intersection before integrating.',
        'clipboard-4201197806.png': 'The contour of a loss function touches the boundary of a constraint set at a constrained optimum.',
    },
}

IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)(?:\{[^}]*\})?')

CALCULUS_IMAGES = {
    'surface-3%20cylinder.jpg': 'surface-three-cylinders.jpg',
    's3.jpg': 'three-cylinder-surface.jpg',
    "method1's%20photo%20behind.png": 'three-cylinder-method-one.png',
    'm3.jpg': 'three-cylinder-cross-sections.jpg',
    '3%20cylinders%20method%202.jpg': 'three-cylinder-method-two.jpg',
    'clipboard-4201197806.png': 'constrained-optimization.png',
}

DOCS = {
    'Mathematical Analysis 1.qmd': 'Math-s-interesting-things-main/docs/Mathematical Analysis 1.html',
    'Calculus.qmd': 'Math-s-interesting-things-main/docs/Calculus.html',
    'mth107.qmd': 'Math-s-interesting-things-main/docs/mth107.html',
    'mth1113.qmd': 'Math-s-interesting-things-main/docs/mth1113.html',
    'stat_learn.qmd': 'Math-s-interesting-things-main/docs/stat_learn.html',
    'mth106.qmd': 'Math-s-interesting-things-main/docs/mth106.html',
    '2024surf.qmd': 'stat.pre-main/docs/2024surf.html',
    'SurveySampling.qmd': 'stat.pre-main/docs/SurveySampling.html',
    'MTH203Project.qmd': 'stat.pre-main/docs/MTH203Project.html',
    'distribution transformation.qmd': 'stat.pre-main/docs/distribution transformation.html',
    'survival_analysis.qmd': 'stat.pre-main/docs/survival_analysis.html',
    'resampling.qmd': 'stat.pre-main/docs/resampling.html',
    'glm pre.qmd': 'stat.pre-main/docs/Linear Models and Regression Analysis/glm pre.html',
    'some tips about stats.qmd': 'stat.pre-main/docs/Linear Models and Regression Analysis/some tips about stats.html',
    'nothing.qmd': 'stat.pre-main/docs/nothing.html',
}

def original_media():
    with zipfile.ZipFile(ZIP) as archive:
        target = MEDIA / 'calculus'
        target.mkdir(parents=True, exist_ok=True)
        for original, renamed in CALCULUS_IMAGES.items():
            old_path = original.replace('%20', ' ')
            prefix = 'Math-s-interesting-things-main/'
            if old_path.startswith('clipboard-'):
                old_path = 'images/' + old_path
            (target / renamed).write_bytes(archive.read(prefix + old_path))

def figure(path, caption):
    return (f'<figure class="note-figure" style="max-width:560px;margin:1.3rem auto;">'
            f'<img src="{path}" alt="{caption}" loading="lazy" style="display:block;max-width:100%;max-height:420px;width:auto;height:auto;margin:auto;object-fit:contain;">'
            f'<figcaption style="font-size:.88rem;color:#666;text-align:center;margin-top:.45rem;">{caption}</figcaption></figure>')

def add_saved_plot_outputs(body, source_name):
    """Place archived Quarto plot outputs immediately after their source chunks."""
    doc = DOCS.get(source_name)
    if not doc:
        return body
    with zipfile.ZipFile(ZIP) as archive:
        if doc not in archive.namelist():
            return body
        soup = BeautifulSoup(archive.read(doc), 'html.parser')
        cells = [c for c in soup.select('div.cell') if c.select_one('div.cell-code')]
        lines = body.splitlines()
        openers = [i for i, line in enumerate(lines) if re.match(r'^```(?:r|python|py) qmd-chunk$', line, re.I)]
        if len(cells) != len(openers):
            print('Skipped plot restoration because chunk counts differ:', source_name, len(cells), len(openers))
            return body
        output_dir = MEDIA / 'code-output' / re.sub(r'[^a-z0-9]+','-',source_name.lower()).strip('-')
        output_dir.mkdir(parents=True, exist_ok=True)
        insertions = {}
        for index, (start, cell) in enumerate(zip(openers, cells), 1):
            images = cell.select('div.cell-output-display img')
            if not images:
                continue
            end = next((j for j in range(start + 1, len(lines)) if lines[j].strip() == '```'), None)
            if end is None:
                continue
            figures = []
            for number, img in enumerate(images, 1):
                src = img.get('src', '')
                archive_path = doc.rsplit('/',1)[0] + '/' + src
                if archive_path not in archive.namelist():
                    continue
                extension = Path(src).suffix.lower() or '.png'
                name = f'chunk-{index:03d}-{number}{extension}'
                (output_dir / name).write_bytes(archive.read(archive_path))
                figures.append(figure('/assets/img/code-output/'+output_dir.name+'/'+name, f'Output from code example {index}'))
            if figures:
                insertions.setdefault(end, []).extend(figures)
        result = []
        for i, line in enumerate(lines):
            result.append(line)
            result.extend(insertions.get(i, []))
        return '\n'.join(result)

def source_body(path):
    text = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    if text.startswith('---\n'):
        text = text.split('\n---\n', 1)[1]
    text = re.sub(r'^```\{([A-Za-z0-9_+.-]+)[^}]*\}', r'```\1 qmd-chunk', text, flags=re.M)
    text = re.sub(r'^#\|.*\n', '', text, flags=re.M)
    return text.strip()

def describe_images(body, source_name):
    heading = 'the current mathematical argument'
    output = []
    last_description = None
    for line in body.splitlines():
        match_heading = re.match(r'^#{1,6}\s+(.+)$', line.strip())
        if match_heading and not IMAGE.search(line):
            heading = match_heading.group(1).strip().rstrip('.:')
        matches = list(IMAGE.finditer(line))
        if not matches:
            output.append(line)
            continue
        descriptions = []
        for m in matches:
            filename = Path(m.group(2).split('#',1)[0]).name
            description = FIGURES.get(source_name, {}).get(filename)
            if not description and m.group(1).strip():
                description = m.group(1).strip().rstrip('.') + '.'
            if not description:
                clean_heading = re.sub(r'[`$*#]', '', heading).strip()
                description = f'This visual example illustrates {clean_heading.lower()}.'
            if source_name == 'Calculus.qmd' and filename in CALCULUS_IMAGES:
                descriptions.append(figure('/assets/img/calculus/'+CALCULUS_IMAGES[filename], description))
                continue
            if description != last_description:
                descriptions.append(description)
                last_description = description
        remainder = IMAGE.sub('', line).strip()
        if remainder.startswith('#') and descriptions:
            output.append(remainder)
            output.extend('')
            output.append(' '.join(descriptions))
        elif remainder in {'', '-', '-   ', 'eg.', 'eg. ', 'ex:'}:
            output.append(' '.join(descriptions))
        else:
            output.append(remainder)
            output.append(' '.join(descriptions))
    return '\n'.join(output)

def fix_stale_figure_references(body):
    return (body
        .replace('The flowchart in Figure1 illustrates the methodology for data cleaning and variable selection in survival analysis.', 'The data-cleaning sequence begins the methodology for variable selection in survival analysis.')
        .replace('This figure2 presents the survival outcomes for several organophosphate pesticide samples.', 'The comparison considers survival outcomes for several organophosphate pesticide samples.')
        .replace('see the photo attached, which is the easiest way for computation:', 'The symmetric surface pieces make the computation easier:')
        .replace('see the photo attached', 'The decomposition is described here.')
        .replace('see photo in particular,', 'In particular,')
        .replace('(or see the attached picture to see more picisely)', '(the nested intervals make this visible)'))

def write_page(filename, title, permalink, body, project=False):
    parent = 'Projects' if project else 'Lecture Notes'
    parent_url = '/projects/' if project else '/math/'
    note_flag = '' if project else 'lecture_note: true\n'
    content = ('---\nlayout: page\ntitle: '+json.dumps(title,ensure_ascii=False)+'\npermalink: '+permalink+
               '\nnav: false\n'+note_flag+'math: true\ntoc:\n  sidebar: left\n---\n\n'+
               f"[← {parent}]({{{{ '{parent_url}' | relative_url }}}})\n\n"+
               '{% raw %}\n'+body.strip().replace(' qmd-chunk','')+'\n{% endraw %}\n')
    path = PAGES / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf8')

def notebook_body():
    notebook=json.loads((MATH/'Simple_ODEs (1).ipynb').read_text(encoding='utf8'))
    parts=['## ODEs and PDEs with codes']
    for i,cell in enumerate(notebook['cells']):
        body=''.join(cell.get('source',[])).strip()
        if i==0:
            body=re.sub(r'^# Thanks to Dr\. Mengqi Hu[^\n]*\n*','',body).strip()
        if not body:
            continue
        if cell['cell_type']=='markdown':
            body=re.sub(r'^#(?!#)', '###', body, flags=re.M)
            body=describe_images(body,'Simple_ODEs (1).ipynb')
            parts.append(body)
        elif cell['cell_type']=='code':
            parts.append('```python\n'+body+'\n```')
            for number, output in enumerate(cell.get('outputs', []), 1):
                data = output.get('data', {})
                if 'image/png' in data:
                    path = MEDIA / 'code-output' / 'simple-odes'
                    path.mkdir(parents=True, exist_ok=True)
                    name = f'cell-{i+1:02d}-{number}.png'
                    (path / name).write_bytes(base64.b64decode(''.join(data['image/png'])))
                    parts.append(figure('/assets/img/code-output/simple-odes/'+name, 'Plot produced by the Python example above'))
    return '\n\n'.join(parts)

def main():
    original_media()
    for filename,title,slug in MATH_PAGES:
        body=fix_stale_figure_references(describe_images(source_body(MATH/filename),filename))
        if slug=='probability-statistics':
            body=body.replace('Given $(\\Omega, \\mathbb{F},\\mathbb{P})$, $\\mathbb{F}$-measurable mapping: X: $\\mathbb{\\Omega} \\to \\mathbb{R}$', 'Given $(\\Omega, \\mathcal{F},\\mathbb{P})$, an $\\mathcal{F}$-measurable mapping $X: \\Omega \\to \\mathbb{R}$')
            body=body.replace('Here, for $\\mathbb{F}$-measurable, it means $\\forall a \\in\\mathbb{R}$, {${\\omega \\in \\Omega|X(\\omega) \\leq a}$}$\\in \\mathbb{F}$', 'Here, measurability means $\\{\\omega \\in \\Omega : X(\\omega) \\leq a\\} \\in \\mathcal{F}$ for every $a \\in \\mathbb{R}$.')
            body=body.replace('P(X=x) = P(${\\omega \\in \\Omega|X(\\omega)=x}$}', '$P(X=x)=P(\\{\\omega \\in \\Omega : X(\\omega)=x\\})$')
        body=add_saved_plot_outputs(body, filename)
        if slug=='probability-statistics':
            aic=source_body(MATH/'APH203.qmd')
            body+='\n\n## Model selection: AIC, AICc, and BIC\n\n'+aic[aic.index('### AIC (Akaike Information Criterion)'):aic.index('### reference',aic.index('### AIC (Akaike Information Criterion)'))].strip()
        write_page('math/'+slug+'.md',title,'/math/'+slug+'/',body)
    ode=fix_stale_figure_references(describe_images(source_body(MATH/'mth106.qmd'),'mth106.qmd'))
    ode=add_saved_plot_outputs(ode,'mth106.qmd')
    write_page('math/differential-equations.md','ODE, PDE, and Fourier Series with codes','/math/differential-equations/',
               '## ODE, PDE, and Fourier Series\n\n'+ode+'\n\n'+notebook_body())
    for filename,title,slug,project in STAT_PAGES:
        body=fix_stale_figure_references(describe_images(source_body(STATS/filename),Path(filename).name))
        body=add_saved_plot_outputs(body, Path(filename).name)
        if slug=='mip-algorithm':
            body=body.replace('https://github.com/yuuuulu/stat.pre/blob/main/MTH203_report.pdf','/assets/pdf/imported/MTH203_report.pdf')
        write_page('statistics/'+slug+'.md',title,'/statistics/'+slug+'/',body,project)

if __name__=='__main__':
    main()
