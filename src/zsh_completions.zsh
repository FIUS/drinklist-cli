#compdef drinklist drink="drinklist drink"

# zsh completion wrapper for drinklist-cli

local -a _drinklist_global_args
_drinklist_global_args=(
   "(-h --help)"{-h,--help}'[Show help]'
   "(-f -format)"{-f,-format}'[Output format]:format:((
       text\:Output\ results\ as\ Human-readable\ table\ or\ text
       json\:Output\ results\ as\ JSON
    ))'
   "(-sort-by)"'-sort-by[Sort by given column]:sortby:_drinklist_arg_column'
   "(-col -columns)"{-col,-columns}'[The columns to show]:columns:_drinklist_arg_columns'
   "(-sort-desc -sort-descending)"{-sort-desc,-sort-descending}'[Sort descending instead of ascending]'
   "(-config -config_file)"{-config,-config_file}'[The config file to use]:file:_files'
   "(--url)"'--url[The API URL of the drinklist]:url:_urls'
   "(-pw)"'-pw[The drinklist password]:pw:_strings'
   "(-u -user)"{-u,-user}'[The username to execute actions for]:user:_drinklist_arg_users'
   "(-cache -cache_file)"{-cache,-cache_file}'[The cache file to use]:file:_files'
   "(-t -token)"{-t,-token}'[The authentication token to use]:token:_strings'
)

function _drinklist_arg_column {
    local -a column
    columns=(
        "name" "stock" "price"
        "balance"
        "id" "user" "reason" "amount" "beverage" "beverage_count" "timestamp"
    )
    _values "columns" $columns[@]
}
function _drinklist_arg_columns {
    _sequence -s " " _drinklist_arg_column
}
function _drinklist_arg_users {
    local -a users
    users=("${(@f)$(drinklist users)}")
    _values "users" "$users[@]"
}
function _drinklist_arg_drinks {
    local -a drinks
    local -a aliases
    drinks=("${(@f)$(drinklist list -columns name | tail +3 | sed 's/[[:blank:]]*$//')}")
    aliases=() # todo
    _values "drinks" "$drinks[@]" "$aliases[@]"
}
function _drinklist_arg_aliases {
    local -a aliases
    aliases=() # todo
    # _values "aliases" "$aliases[@]"
    _strings # for now
}
function _drinklist_commands {
    local -a commands
    commands=(
        'list:List available drinks'
        'drink:Order a drink'
        'order:Order a drink'
        'users:List users of this drinklist'
        'balance:Get current drinklist balance'
        'history:Get drinklsit history'
        'refresh_token:Refresh authentication token'
        'alias:Commands regarding aliases for drinks'
        'undo:Undo last order'
        'license:Show license'
        'help:Show help'
    )
    _describe 'command' commands
}

function _drinklist {
    local line
    local -a args

    _arguments -C $_drinklist_global_args[@] \
               "1: :_drinklist_commands" \
               "*::arg:->args"

    case $line[1] in
        list) _drinklist_list ;;
        drink) _drinklist_drink ;;
        order) _drinklist_drink ;;
        users) _drinklist_users ;;
        balance) _drinklist_balance ;;
        history) _drinklist_history ;;
        refresh_token) _drinklist_refresh_token ;;
        alias) _drinklist_alias ;;
        undo) _drinklist_undo ;;
        license) _drinklist_license ;;
        help) _drinklist_help ;;
    esac
}
function _drinklist_list {
    local -a list_args
    list_args=(
        "(-r -re -regex)"{-r,-re,-regex}'[Regex to filter results by]:regex:_strings'
    )
    _arguments -C $list_args[@] $_drinklist_global_args[@] \
               "*::arg:->args"
}
function _drinklist_drink {
    _arguments -C "1: :_drinklist_arg_drinks"
}
function _drinklist_users {
    _arguments -C "(-h --help)"{-h,--help}'[Show help]' \
               "*::arg:->args"
}
function _drinklist_balance {
    local -a balance_args
    balance_args=(
        "(-a -all)"{-a,-all}'[Show balances for all users]'
    )
    _arguments -C $balance_args[@] $_drinklist_global_args[@] \
               "*::arg:->args"
}
function _drinklist_history {
    local -a history_args
    histoy_args=(
        "(-a -all)"{-a,-all}'[Show history for all users]'
    )
    _arguments -C $history_args[@] $_drinklist_global_args[@] \
               "*::arg:->args"
}
function _drinklist_refresh_token {
    _arguments -C $_drinklist_global_args[@] \
               "*::arg:->args"
}
function _drinklist_alias_commands {
    local -a alias_commands
    alias_commands=(
        "list:List all defined aliases"
        "delete:Delte a defined alias"
        "set:Add a new alias"
    )
    _describe "alias_commands" alias_commands
}
function _drinklist_alias {
    _arguments -C "(-h --help)"{-h,--help}'[Show help]' \
               "1: :_drinklist_alias_commands" \
               "*::arg:->args"

    case $line[1] in
        list) _drinklist_alias_list ;;
        delete) _drinklist_alias_delete ;;
        set) _drinklist_alias_set ;;
    esac
}
function _drinklist_alias_list {
    _arguments -C "(-h --help)"{-h,--help}'[Show help]' \
               "*::arg:->args"
}
function _drinklist_alias_delete {
    _arguments -C "(-h --help)"{-h,--help}'[Show help]' \
               "1: :_drinklist_arg_aliases" \
               "*::arg:->args"
}
function _drinklist_alias_set {
    _arguments -C "(-h --help)"{-h,--help}'[Show help]' \
               "1: :_strings" \
               "2: :_drinklist_arg_drinks" \
               "*::arg:->args"
}
function _drinklist_undo {
    _arguments -C "(-h --help)"{-h,--help}'[Show help]' \
               "*::arg:->args"
}
function _drinklist_license {
    _arguments -C "(-h --help)"{-h,--help}'[Show help]' \
               "*::arg:->args"
}
function _drinklist_help {
    function _subcommands {
        case $line[1] in
            alias) _drinklist_alias_commands ;;
            *) _values "test" "$line[1]" "$line[@]" "$line[*]"
        esac
    }
    _arguments -C "(-h --help)"{-h,--help}'[Show help]' \
               "1: :_drinklist_commands" \
               "2: :_subcommands" \
               "*::arg:->args"
}
