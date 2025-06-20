#!/usr/bin/env bash
#
# Run Python code tools (isort, black, flake8)
#
#### SETUP ####################################################################

set -o errexit
set -o errtrace
set -o nounset

# shellcheck disable=SC2154
trap '_es=${?};
    printf "${0}: line ${LINENO}: \"${BASH_COMMAND}\"";
    printf " exited with a status of ${_es}\n";
    exit ${_es}' ERR

DIR_REPO="$(cd -P -- "${0%/*}/.." && pwd -P)"
# https://en.wikipedia.org/wiki/ANSI_escape_code
E0="$(printf "\e[0m")"        # reset
E30="$(printf "\e[30m")"      # black foreground
E31="$(printf "\e[31m")"      # red foreground
E107="$(printf "\e[107m")"    # bright white background

#### FUNCTIONS ################################################################

check_docker() {
    local _msg
    if ! docker compose exec web true 2>/dev/null; then
        _msg='The app container/services is not avaialable.'
        _msg="${_msg}\n       First run \`docker compose up\`."
        error_exit "${_msg}"
    fi
}

error_exit() {
    # Echo error message and exit with error
    echo -e "${E31}ERROR:${E0} ${*}" 1>&2
    exit 1
}

icon_stats() {
    local _count _size
    print_header 'Icons stats'
    echo '/srv/licensebuttons/www/i'
    _count=$(docker compose exec web find /srv/licensebuttons/www/i -type f \
        | wc -l | tr -d '[:space:]')
    _size=$(docker compose exec web du -sh /srv/licensebuttons/www/i \
        | awk '{print $1}')
    printf '    %11s %5s\n'  'File count:' "${_count}"
    printf '    %11s %5s\n'  'Size:' "${_size}"
    echo
}

print_header() {
    # Print 80 character wide black on white heading with time
    printf "${E30}${E107}# %-69s$(date '+%T') ${E0}\n" "${@}"
}

#### MAIN #####################################################################

cd "${DIR_REPO}"

check_docker

icon_stats

print_header 'Generate icons in Docker container'
docker compose exec web \
    /usr/bin/python3 /srv/licensebuttons/scripts/genicons.py
echo 'done.'
echo

icon_stats
