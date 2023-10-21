declare -Ag websearch=(
    # Syntax:
    # [name]="https://www.example.com/search?q="
    # Search Engines
    [bing]="https://www.bing.com/search?q="
    [brave]="https://search.brave.com/search?q="
    [duckduckgo]="https://duckduckgo.com/?q="
    [google]="https://www.google.com/search?q="
    [yandex]="https://yandex.com/search/?text="
    # Information/News
    [googlenews]="https://news.google.com/search?q="
    [wikipedia]="https://en.wikipedia.org/w/index.php?search="
    [wiktionary]="https://en.wiktionary.org/w/index.php?search="
    # Media
    [reddit]="https://www.reddit.com/search/?q="
    [youtube]="https://www.youtube.com/results?search_query="
    # Shopping
    [amazon]="https://www.amazon.in/s?k="
    [flipkart]="https://www.flipkart.com/search?q="
    [jiomart]="https://www.jiomart.com/search/"
    [bigbasket]="https://www.bigbasket.com/ps/?q="
    # Linux
    [archaur]="https://aur.archlinux.org/packages/?O=0&K="
    [archpkg]="https://archlinux.org/packages/?sort=&q="
    [archwiki]="https://wiki.archlinux.org/index.php?search="
    [debianpkg]="https://packages.debian.org/search?suite=default&section=all&arch=any&searchon=names&keywords="
    # development
    [github]="https://github.com/search?q="
    [gitlab]="https://gitlab.com/search?search="
    [googleOpenSource]="https://opensource.google/projects/search?q="
    [sourceforge]="https://sourceforge.net/directory/?q="
    [stackoverflow]="https://stackoverflow.com/search?q="
)

main() {
    if [ -z "${!websearch[*]}" ]; then
        echo "$(date): dm-websearch: BREAKING CHANGES: Due to breaking changes you must edit all declare statements in your config to include the g option. declare -A -> declare -Ag, declare -a -> declare -ag"
        sleep 2
        exit 1
    fi

    engine=$(printf '%s\n' "${!websearch[@]}" | sort | ${MENU} 'Choose search engine:') || exit 1
    url="${websearch["${engine}"]}"
    prompt="Search ${engine}"
    MENU="${MENU:0:34} -theme ./themes/fullInputWidth ${MENU:34}"
    echo $MENU
    query=$(${MENU} "${prompt}")
    query="$(echo -n "${query}" | jq -s -R -r @uri)"
    if [ -z "$query" ]; then
        exit 0
    fi
    google-chrome-stable "${url}${query}"
}

MENU="rofi -no-show-icons -sort -sorting-method fzf -i -dmenu -p "
[[ "${BASH_SOURCE[0]}" == "${0}" ]] && main