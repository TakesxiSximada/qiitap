Add include function to Qiita Markdown
======================================

Why
---

By adding a positionable specifying feature to Markdown, you can test code snippets in Markdown.


Install
-------

::

   $ pip install qiitap


How to use it
-------------

Create Authentication files.

::

   $ qiitap auth

Create an article on Qiita.

::

   $ qiitap create qiita.md --no-body

It create qiita.md file.

Update the article on Qiita

::

   $ qiitap update qiita.md

It update the article.

Include other file content in your markdown file.

qiita.md::

    <!---
    <%namespace name="qiitap" module="qiitap"/>
    <%doc>
    title: "This article's title"
    item_id: 6fa704dffd25dce635e2
    tags:
        - name: Qiita
        - name: Python
    private: True
    </%doc>
    --->

    ```text:AllContent
    ${qiitap.qinclude('./fish.md')}
    ```

    ```text:SubContent
    ${qiitap.qinclude('./fish.md', start_at='START', end_at='END')}
    ```
