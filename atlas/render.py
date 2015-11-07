import html
import os

from .util import wrap


class Renderer:

    def __init__(self, story):
        self.story = story

    def basename(self):
        return ''.join('-' if c == ' ' else c
                       for c in self.story.title
                       if c not in '.:/\\')

    def filename(self):
        return '{}.{}'.format(self.basename(),
                              self.file_ext().lstrip('.'))

    def file_ext(self):
        yield TypeError('Subclasses must implement this method')

    def render(self):
        yield TypeError('Subclasses must implement this method')

    def render_file(self, dirname, verbose=True):
        text = self.render()

        path = os.path.join(dirname, self.filename())
        if verbose:
            print('Writing to {}'.format(path))

        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(text)


#------------------------------------------------------------------------------
# Markdown

class MarkdownRenderer(Renderer):

    def file_ext(self):
        return 'markdown'

    def render(self):
        story = self.story

        blocks = [
            self.render_heading(story.title, primary=True),
            self.render_heading('Contents'),
        ]

        contents, body = [], []
        for chapter in story:
            title = html.escape(chapter.title)
            subtitle = html.escape(chapter.subtitle)
            slug = chapter.slug

            contents.append('{num}. [{title}](#{slug})'.format_map({
                'num': chapter.number,
                'title': '**{}** ({})'.format(title, subtitle),
                'slug': slug,
            }))

            body.append(self.render_heading(
                '{} ({})'.format(title, subtitle),
                slug=slug))

            for paragraph in chapter:
                body.append(wrap(html.escape(paragraph)))

        blocks.append('\n'.join(contents))
        blocks += body
        return '\n\n'.join(blocks) + '\n'

    def render_heading(self, title, primary=False, slug=None):
        prefix = '# ' if primary else '## '
        link = '<a name="{}"></a>'.format(slug) if slug else ''
        return ''.join((prefix, link, title))


#------------------------------------------------------------------------------
# HTML

HTML_TEMPLATE = """\
<article>
    <h1>{title}</h1>

    <section>
        <h1>Contents</h1>
        <ol>
            {contents}
        </ol>
    </section>

    {chapters}
</article>
"""

HTML_CHAPTER_TEMPLATE = """\
    <section>
        <header>
            <h1><a name="{slug}"></a>{title}</h1>
            <h2>{subtitle}</h2>
        </header>

        {paragraphs}
    </section>
"""

class HtmlRenderer(Renderer):

    def file_ext(self):
        return 'html'

    def render(self):
        story = self.story
        contents_indent = ' ' * 12
        chapter_indent = ' ' * 8

        contents, chapters = [], []
        for chapter in story:
            title = html.escape(chapter.title)
            subtitle = html.escape(chapter.subtitle)
            slug = chapter.slug

            contents.append(
                '<li><a href="#{}"><b>{}</b> ({})</a></li>'
                .format(slug, title, subtitle))

            paragraphs = (wrap('<p>{}</p>'.format(html.escape(par)),
                               indent=chapter_indent)
                          for par in chapter)

            chapters.append(HTML_CHAPTER_TEMPLATE.format_map({
                'title': title,
                'subtitle': subtitle,
                'slug': slug,
                'paragraphs': '\n\n'.join(paragraphs).lstrip(),
            }))

        return HTML_TEMPLATE.format_map({
            'title': html.escape(story.title),
            'contents': ('\n' + contents_indent).join(contents),
            'chapters': '\n'.join(chapters).lstrip(),
        })


#------------------------------------------------------------------------------

RENDERERS = [
    MarkdownRenderer,
    HtmlRenderer,
]
