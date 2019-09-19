#!/usr/bin/env bash
_DRINKLIST_COMMAND="drinklist" #This is the command you use for the complete drinklist cli.
_DRINKLIST_COMMAND_ALIAS_DRINK="drink" #This is the alias you use for "<COMMAND> drink". If you don't want this set to empty string.

_DRINKLIST_CACHE_DIR="/tmp/_drinklist"
_DRINKLIST_CACHE_DURATION="5" #In minutes

_DRINKLIST_FLAGS=( "-h" "--help" "-format" "-sort-by" "-columns" "-sort-descending" "-config" "-url" "-token" "-user" )
_DRINKLIST_FLAGS_WITH_ARGS=( "-format" "-sort-by" "-columns" "-config" "-url" "-token" "-user" )
_DRINKLIST_COMMANDS=( "list" "drink" "order" "users" "balance" "history" "refresh_token" "alias" "license" "help" "undo" )

function _drinklist_check_cache {
  if ! [ -d $_DRINKLIST_CACHE_DIR ] ;then
    mkdir "$_DRINKLIST_CACHE_DIR"
  fi

  find "$_DRINKLIST_CACHE_DIR" -mmin "+$_DRINKLIST_CACHE_DURATION" -type f -delete
}

function _drinklist_containsElement {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

function _drinklist_getCommand {
  for word in "${COMP_WORDS[@]}" ;do
    if _drinklist_containsElement "$word" "${_DRINKLIST_COMMANDS[@]}" ;then
      echo $word
      return 0
    fi
  done
  return 1
}

function _drinklist_prepare {
  _drinklist_compopts=()
  _drinklist_cur="${COMP_WORDS[COMP_CWORD]}"
  _drinklist_prev="${COMP_WORDS[COMP_CWORD-1]}"
  _drinklist_options=""
}

function _drinklist_finish {
  COMPREPLY=()
  while read _drinklist_line ;do
    printf -v _drinklist_comprep "%q" "$_drinklist_line"
    COMPREPLY=( "${COMPREPLY[@]}" "$_drinklist_comprep" )
  done << EOF 
$(compgen -o default -W "$(echo "${_drinklist_compopts[@]}")" -- ${_drinklist_cur})
EOF
}

function _drinklist_flags {
  if [[ "$_drinklist_cur" == "-"* ]] || [ ${#_drinklist_compopts[@]} -eq 0 ] ;then
    _drinklist_compopts=( "${_drinklist_compopts[@]}" "${_DRINKLIST_FLAGS[@]}" )
  else
    _drinklist_compopts=( "${_drinklist_compopts[@]}" "- " " " )
  fi  
}

function _drinklist_flag_arguments {
  if _drinklist_containsElement "$_drinklist_prev" "${_DRINKLIST_FLAGS_WITH_ARGS[@]}" ;then
    #TODO: Add argument completion for flags which don't take files.
    return 0
  else
    return 1
  fi
}

function _drinklist_get_drink_names {
  _drinklist_drink_names=()
  _drinklist_check_cache
  if ! [ -f "$_DRINKLIST_CACHE_DIR/drink_names" ] ;then
    $_DRINKLIST_COMMAND list -columns name > "$_DRINKLIST_CACHE_DIR/drink_names"
  fi

  _drinklist_lines_to_skip=2
  while read _drinklist_line ;do
    if [ $_drinklist_lines_to_skip -gt 0 ] ;then
      let "_drinklist_lines_to_skip =  $_drinklist_lines_to_skip - 1"
    else
      printf -v _drinklist_name "%q" "$_drinklist_line"
      _drinklist_drink_names=( "${_drinklist_drink_names[@]}" "$_drinklist_name" )
    fi
  done < "$_DRINKLIST_CACHE_DIR/drink_names"
}

function _drinklist_drinks {
  _drinklist_get_drink_names
  _drinklist_compopts=( "${_drinklist_compopts[@]}" "${_drinklist_drink_names[@]}" )
}

function _drinklist_normal {
  _drinklist_command=$(_drinklist_getCommand)
  _drinklist_ret=$?
  if ! (return $_drinklist_ret) ;then
    _drinklist_compopts=( "${_drinklist_compopts[@]}" "${_DRINKLIST_COMMANDS[@]}" )
  else
    if [ "$_drinklist_command" == "drink" ] ;then
      _drinklist_drinks
    fi
    #TODO make more commands completable
  fi

  _drinklist_flags
}

function _drinklist_alias_normal {
  _drinklist_drinks
  _drinklist_flags
}

function _drinklist_alias {
  _drinklist_prepare

  _drinklist_flag_arguments ||
  _drinklist_alias_normal

  _drinklist_finish
}

function _drinklist {
  _drinklist_prepare

  _drinklist_flag_arguments || 
  _drinklist_normal

  _drinklist_finish
}

complete -F _drinklist $_DRINKLIST_COMMAND

if ! [ "$_DRINKLIST_COMMAND_ALIAS_DRINK" == "" ] ;then
  complete -F _drinklist_alias $_DRINKLIST_COMMAND_ALIAS_DRINK
fi
