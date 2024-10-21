package main

import (
	"context"
	"fmt"
	"github.com/danielgtaylor/huma/v2"
	"github.com/danielgtaylor/huma/v2/adapters/humachi"
	"github.com/go-chi/chi/v5"
	"net/http"

	_ "github.com/danielgtaylor/huma/v2/formats/cbor"
)

/*
- fix to do proper basic authentication as for the FastAPI spec, update description
*/

const (
	username        = "sAmTh3MiNut3mAn"
	password        = "apisAreCool@#88"
	validAuthHeader = "c0FtVGgzTWlOdXQzbUFuOmFwaXNBcmVDb29sQCM4OA==" //TODO: proper var name?
	flagPart1       = "UMASS{auth0riz"
	flagPart2       = "At!ion-Is-c00l}"
)

var (
	api             huma.API
	returnFlagPart2 = false
)

func main() {
	router := chi.NewMux()
	api = humachi.New(router, huma.DefaultConfig("My API", "1.0.0"))

	setupEndpoints()

	http.ListenAndServe("127.0.0.1:8888", router)
}

// TODO: make sure methods that don't need to be public arent
func authorizeBearerToken(ctx huma.Context, next func(huma.Context)) {
	authBearerHeader := ctx.Header("Authorization") //TODO: fix variable name
	if authBearerHeader != fmt.Sprintf("Basic %s", validAuthHeader) {
		huma.WriteErr(api, ctx, http.StatusForbidden,
			"Are you sure you are Sam the Minuteman?", fmt.Errorf("unauthorized request"),
		)
		return
	}
	next(ctx)
}

func GetPasswordMiddleware(ctx huma.Context, next func(huma.Context)) {
	if username != ctx.Query("username") {
		huma.WriteErr(api, ctx, http.StatusBadRequest,
			"Are you sure you know my name?", fmt.Errorf("bad request"),
		)
		return
	}
	next(ctx)
}

// move to types file TODO
type GetUsernameInput struct {
}
type GetPasswordInput struct {
	Username string `query:"username" maxLength:"30"`
}

type GetSecret1Input struct {
	Auth string `header:"Authorization" default:"Basic"`
}
type PostSecret2Input struct {
	Body struct {
		SecretPart1 string `json:"secretPart1"`
	}
}

type Output struct {
	Body struct {
		Message string `json:"message"`
	}
}

func setupEndpoints() {
	huma.Register(api, huma.Operation{
		OperationID: "get-name",
		Method:      http.MethodGet,
		Path:        "/name",
		Summary:     "Get my name",
		Description: "The server will want my username later.",
	}, func(ctx context.Context, input *GetUsernameInput) (*Output, error) {
		resp := &Output{}
		resp.Body.Message = fmt.Sprintf("My name is %s", username)
		return resp, nil
	})

	huma.Register(api, huma.Operation{
		OperationID: "get-password-if-sam",
		Method:      http.MethodGet,
		Path:        "/password",
		Middlewares: huma.Middlewares{GetPasswordMiddleware},
		Summary:     "Get my password",
		Description: "I will give you my password if you know my name.",
	}, func(ctx context.Context, input *GetPasswordInput) (*Output, error) {
		resp := &Output{}
		resp.Body.Message = fmt.Sprintf("My password is %s", password)
		return resp, nil
	})

	huma.Register(api, huma.Operation{
		OperationID: "get-secret-part1",
		Method:      http.MethodGet,
		Path:        "/secret1",
		Middlewares: huma.Middlewares{authorizeBearerToken},
		Summary:     "Get the beginning of my secret",
		Description: "I love basic tokens!",
	}, func(ctx context.Context, input *GetSecret1Input) (*Output, error) {
		resp := &Output{}
		resp.Body.Message = flagPart1
		return resp, nil
	})

	huma.Register(api, huma.Operation{
		OperationID: "post-secret-part2",
		Method:      http.MethodPost,
		Path:        "/secret2",
		Middlewares: huma.Middlewares{},
		Summary:     "Get the ending of my secret",
		Description: "Give me the beginning of my secret so I can give you the end.",
	}, func(ctx context.Context, input *PostSecret2Input) (*Output, error) {
		fmt.Print(input)
		resp := &Output{}
		if input.Body.SecretPart1 == flagPart1 {
			resp.Body.Message = flagPart2
		} else {
			resp.Body.Message = "Try Again! Are you sure you have the correct beginning of the flag?"
		}
		return resp, nil
	})
}
