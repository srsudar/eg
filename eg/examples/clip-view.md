# clip-view

render specific local pages

    clip-view path/to/page1.clip path/to/page2.clip ...

render specific remote pages

    clip-view page_name1 page_name2 ...

render pages by a specific render

    clip-view --render tldr|tldr-colorful|docopt|docopt-colorful page_name1 page_name2 ...

render pages with a specific color theme

    clip-view --theme path/to/local_theme.yaml|remote_theme_name page_name1 page_name2 ...

clear a page or theme cache

    clip-view --clear-page|--clear-theme-cache

display help

    clip-view --help

display version

    clip-view --version
