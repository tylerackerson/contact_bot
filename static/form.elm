port module Form exposing (..)

import Html.App
import Html exposing (..)
import Html.Events exposing (..)
import Html.Attributes exposing (id, placeholder, type', for, value, class, classList)


view model =
    div [ id "contact" ]
        [ form
            [ id "form"
            , classList
                [ ( "hidden", model.status == "chatting" )
                ]
            ]
            [ h1 [] [ text "Contact" ]
            , label [ for "name" ] [ text "name: " ]
            , input
                [ id "name-field"
                , type' "name"
                , value model.name
                , onInput (\str -> { msgType = "name", payload = str })
                ]
                []
            , label [ for "email-field" ] [ text "email: " ]
            , input
                [ id "email-field"
                , type' "text"
                , value model.email
                , onInput (\str -> { msgType = "email", payload = str })
                ]
                []
            , div [ onClick ({ msgType = "start", payload = "" }), class "button" ] [ text "Start Chat" ]
            ]
        , div
            [ id "chat-window"
            , classList
                [ ( "hidden", model.status == "none" )
                ]
            ]
            [ div [ id "messages" ] []
            , input
                [ id "chat-input"
                , type' "text"
                , placeholder "type message here..."
                , value model.input
                , onInput (\str -> { msgType = "input", payload = str })
                ]
                []
            ]
        ]


port start : String -> Cmd msg


initialModel =
    { name = "", email = "", input = "", status = "none" }


main =
    Html.App.program
        { init = ( initialModel, Cmd.none )
        , view = view
        , update = update
        , subscriptions = \_ -> Sub.none
        }


update msg model =
    if msg.msgType == "start" then
        ( { model | status = "chatting" }, start model.name )
    else if msg.msgType == "name" then
        ( { model | name = msg.payload }, Cmd.none )
    else if msg.msgType == "email" then
        ( { model | email = msg.payload }, Cmd.none )
    else if msg.msgType == "input" then
        ( { model | input = msg.payload }, Cmd.none )
    else
        ( model, Cmd.none )
