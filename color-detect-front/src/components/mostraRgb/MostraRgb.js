import { Component } from "react"
import { PrincipalMostrarRgb, Header, Content, ContentCol01, ContentCol01Linha02, InputHabilitaCor, MostradorDeCor, AjusteMinimo, Title, Input } from "./styles"


export default class MostrarRgb extends Component {

    constructor (props) {
        super(props)

        this.state = {
            cor: props.cor,
            h: 255,
            s: 255,
            v: 255,
            habilitaEditarCor: false,
        }
    }


    componentWillReceiveProps = (props) => {
        let hsv = props.cor

        let arrayHsv = hsv.split(',')

        let h = parseInt(arrayHsv[0])
        let s = parseInt(arrayHsv[1])
        let v = parseInt(arrayHsv[2])

        if (!this.state.habilitaEditarCor) {
            this.setState({
                cor: hsv,
                h: h,
                s: s,
                v: v,
            })
        }
    }

    habilitaEdicao = (e) => {
        this.setState({
            habilitaEditarCor: e.target.checked
        })
    }

    modificarCorR = (e) => {
        let h = parseInt(e.target.value)
        let s = parseInt(this.state.s)
        let v = parseInt(this.state.v)

        let cor = `${h},${s}%,${v}%`

        this.props.newColor(cor)

        this.setState({
            cor: cor,
            h: h
        })
    }

    modificarCorG = (e) => {
        let h = parseInt(this.state.h)
        let s = parseInt(e.target.value)
        let v = parseInt(this.state.v)

        let cor = `${h},${s}%,${v}%`

        this.props.newColor(cor)

        this.setState({
            cor: cor,
            s: s
        })
    }

    modificarCorB = (e) => {
        let h = parseInt(this.state.h)
        let s = parseInt(this.state.s)
        let v = parseInt(e.target.value)

        let cor = `${h},${s}%,${v}%`

        this.props.newColor(cor)

        this.setState({
            cor: cor,
            v: v
        })
    }

    render() {
        return (
            <PrincipalMostrarRgb>
                <Header>
                    <Title>{this.props.title}</Title>
                </Header>
                <Content>
                    <InputHabilitaCor type='checkbox' onChange={this.habilitaEdicao}></InputHabilitaCor>
                    <MostradorDeCor style={{ backgroundColor: `hsl(${this.state.cor})` }}></MostradorDeCor>
                    <ContentCol01>
                        <ContentCol01Linha02>
                            <p>H</p>
                            <Input type='number' value={this.state.h} onChange={this.modificarCorR} min='0' max='359'></Input>
                            <p>S</p>
                            <Input type='number' value={this.state.s} onChange={this.modificarCorG} min='0' max='100'></Input>
                            <p>V</p>
                            <Input type='number' value={this.state.v} onChange={this.modificarCorB} min='0' max='100'></Input>
                        </ContentCol01Linha02>
                    </ContentCol01>
                </Content>
            </PrincipalMostrarRgb>
        )
    }
}