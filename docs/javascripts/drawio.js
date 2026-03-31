const DRAWIO_SELECTOR = 'img[src$=".drawio"], img[src$=".drawio.svg"]';

function getDiagramConfig(img) {
  const toolbar = ['pages', 'tags', 'zoom', 'layers', 'lightbox'].join(' ');
  const config = {
    toolbar,
    'toolbar-position': 'bottom',
    'toolbar-nohide': '0',
    tooltips: '1',
    border: 5,
    resize: '1',
    edit: '_blank',
    lightbox: '1',
  };

  const zoom = img.getAttribute('zoom');
  if (zoom) {
    config.zoom = zoom;
  }

  return config;
}

function serializeDiagram(xmlText, pageName) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(xmlText, 'application/xml');
  const mxfile = doc.querySelector('mxfile');

  if (!mxfile) {
    const svg = doc.documentElement;
    if (svg && svg.localName === 'svg') {
      return new XMLSerializer().serializeToString(svg);
    }
    return '';
  }

  if (!pageName) {
    return new XMLSerializer().serializeToString(mxfile);
  }

  const matchedPages = Array.from(mxfile.querySelectorAll('diagram')).filter(
    (diagram) => diagram.getAttribute('name') === pageName,
  );

  if (matchedPages.length === 1) {
    const result = doc.implementation.createDocument('', mxfile.tagName, null);
    const root = result.documentElement;
    for (const attr of mxfile.attributes) {
      root.setAttribute(attr.name, attr.value);
    }
    root.appendChild(result.importNode(matchedPages[0], true));
    return new XMLSerializer().serializeToString(root);
  }

  return new XMLSerializer().serializeToString(mxfile);
}

async function replaceDrawioImage(img) {
  if (img.dataset.drawioProcessed === '1') {
    return;
  }

  img.dataset.drawioProcessed = '1';

  const config = getDiagramConfig(img);
  const src = img.getAttribute('src');
  const page = img.getAttribute('page') || img.getAttribute('alt') || '';
  const style = img.getAttribute('style') || '';

  if (/^https?:\/\//i.test(src)) {
    config.url = src;
  } else {
    const response = await fetch(src);
    if (!response.ok) {
      throw new Error(`Failed to fetch drawio diagram: ${src}`);
    }
    const xmlText = await response.text();
    config.xml = serializeDiagram(xmlText, page);
  }

  const div = document.createElement('div');
  div.className = 'mxgraph';
  div.setAttribute('style', `max-width:100%;border:1px solid transparent;${style}`);
  div.setAttribute('data-mxgraph', JSON.stringify(config));
  img.replaceWith(div);
}

async function renderDrawio(root = document) {
  const images = Array.from(root.querySelectorAll(DRAWIO_SELECTOR));
  if (images.length === 0) {
    return;
  }

  await Promise.all(images.map(async (img) => {
    try {
      await replaceDrawioImage(img);
    } catch (error) {
      console.error(error);
      img.dataset.drawioProcessed = '0';
    }
  }));

  if (window.GraphViewer && typeof window.GraphViewer.processElements === 'function') {
    window.GraphViewer.processElements();
  }

  if (typeof window.reload === 'function') {
    window.reload();
  }
}

function scheduleRender(root = document, attempt = 0) {
  if (window.GraphViewer && typeof window.GraphViewer.processElements === 'function') {
    renderDrawio(root);
    return;
  }

  if (attempt < 20) {
    window.setTimeout(() => scheduleRender(root, attempt + 1), 100);
  }
}

window.addEventListener('load', () => scheduleRender());

if (typeof document$ !== 'undefined' && document$ && typeof document$.subscribe === 'function') {
  document$.subscribe(({ body }) => scheduleRender(body));
}

document.addEventListener('change', (event) => {
  if (event.target.matches('.tabbed-set > input')) {
    scheduleRender();
  }
});
