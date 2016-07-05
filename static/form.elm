module Form exposing (..)

import Html.App
import Html exposing (..)
import Html.Events exposing (..)
import Html.Attributes exposing (id, type', for, value, class)


view model =
    form [ id "form" ]
        [ h1 [] [ text "Contact" ]
        , label [ for "name" ] [ text "name: " ]
        , input [ id "name-field", type' "name", value model.name ] []
        , label [ for "email-field" ] [ text "email: " ]
        , input [ id "email-field", type' "text", value model.email ] []
        , div [ class "button" ] [ text "Start Chat" ]
        ]


main =
    view { name = "", email = "" }
