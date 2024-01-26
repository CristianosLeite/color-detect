import { Component } from "react"
import axios from 'axios'
import Swal from "sweetalert2"

import {
    PrincipalHome,
    Header, VisuVideo, ButtonGreen, ButtonBlue,
    Logo, Titulo, Footer, Content, ContentCol01, ContentCol02,
    ContentCol03, ContentCol02Linha01, ContentCol02Linha02,
    ContentCol03Linha01, ContentCol03Linha02, TituloFuncao, HeaderFuncao
} from './styles'

import MostrarRgb from '../mostraRgb/MostraRgb'
import AjusteMascara from "../ajusteMascara/AjusteMascara"
import ConfigCamera from "../configCamera/configCamera"
import Plc from "../plc/Plc"

import LogoUrl from '../../images/logo.png'


export default class Home extends Component {


    constructor (props) {
        super(props)

        this.contexto = {}

        this.state = {
            urlCamera: '',
            urlCameraAux01: '',
            urlCameraAux02: '',
            corInicialMin: '255,255,255',
            corInicialMax: '255,255,255',
            newColormin: '',
            newColormax: '',
        }

        this.urlFrame = this.state.urlCamera
    }

    rgb2hsv = (r, g, b) => {
        var computedH = 0
        var computedS = 0
        var computedV = 0

        //remove spaces from input RGB values, convert to int
        var r = parseInt(('' + r).replace(/\s/g, ''), 10)
        var g = parseInt(('' + g).replace(/\s/g, ''), 10)
        var b = parseInt(('' + b).replace(/\s/g, ''), 10)

        if (r == null || g == null || b == null ||
            isNaN(r) || isNaN(g) || isNaN(b)) {
            alert('Please enter numeric RGB values!')
            return
        }
        if (r < 0 || g < 0 || b < 0 || r > 255 || g > 255 || b > 255) {
            alert('RGB values must be in the range 0 to 255.')
            return
        }
        r = r / 255; g = g / 255; b = b / 255
        var minRGB = Math.min(r, Math.min(g, b))
        var maxRGB = Math.max(r, Math.max(g, b))

        // Black-gray-white
        if (minRGB == maxRGB) {
            computedV = minRGB
            return [0, 0, computedV]
        }

        // Colors other than black-gray-white:
        var d = (r == minRGB) ? g - b : ((b == minRGB) ? r - g : b - r)
        var h = (r == minRGB) ? 3 : ((b == minRGB) ? 1 : 5)
        computedH = 60 * (h - d / (maxRGB - minRGB))
        computedS = ((maxRGB - minRGB) / maxRGB) * 100
        computedV = maxRGB * 100
        return [parseInt(computedH), parseInt(computedS), parseInt(computedV)]
    }

    getFrame = async () => {
        var img = new Image()
        img.crossOrigin = "Anonymous"

        this.contexto = this.canvasA.getContext('2d')

        img.src = this.state.urlCameraAux01

        img.onload = () => {
            img.src = this.state.urlCameraAux01
            this.contexto.drawImage(img, 0, 0)
        }
    }

    getPixelColor = (e) => {
        e.preventDefault()

        console.log(e)

        if (this.contexto.getImageData) {
            const {
                data
            } = this.contexto.getImageData(e.nativeEvent.offsetX, e.nativeEvent.offsetY, 1, 1)

            let hsv = this.rgb2hsv(data[0], data[1], data[2])

            const cor = `${hsv[0]}, ${hsv[1]}%, ${hsv[2]}%`

            this.setState({
                corInicialMin: cor,
                corInicialMax: cor,
                newColormin: cor,
                newColormax: cor,
            })


        }

    }

    startVideo = async () => {
        await this.setState({
            urlCameraAux01: this.state.urlCameraAux02
        })

        this.getFrame()
    }

    stopVideo = () => {
        this.setState({
            urlCameraAux01: ''
        })
    }

    updateColormin = (newColor) => {
        this.setState({
            newColormin: newColor
        })
    }

    updateColormax = (newColor) => {
        this.setState({
            newColormax: newColor
        })
    }

    updateUrlCamera = async (urlCamera) => {
        await this.setState({
            urlCamera: urlCamera,
            urlCameraAux01: urlCamera,
            urlCameraAux02: urlCamera
        })

        this.getColor()
        this.getFrame()
    }

    getColor = () => {
        axios.get(`${this.state.urlCamera}/color`, {timeout: 3000})
            .then(response => {
                let data = response.data
                if (data) {
                    console.log(data)
                    let limitMin = data.limit.colormin.split(',')
                    let limitMax = data.limit.colormax.split(',')
                    let sMin = parseInt(parseInt(limitMin[1]) / 2.55)
                    let vMin = parseInt(parseInt(limitMin[2]) / 2.55)
                    let sMax = parseInt(parseInt(limitMax[1]) / 2.55)
                    let vMax = parseInt(parseInt(limitMax[2]) / 2.55)

                    this.setState({
                        corInicialMin: `${limitMin[0]},${sMin}%,${vMin}%`,
                        corInicialMax: `${limitMax[0]},${sMax}%,${vMax}%`,
                        newColormin: `${limitMin[0]},${sMin}%,${vMin}%`,
                        newColormax: `${limitMax[0]},${sMax}%,${vMax}%`
                    })
                }

            })
            .catch(error => {
                Swal.fire({
                    icon: 'error',
                    title: 'Ops.',
                    text: 'Ocorreu algum erro ao conectar ao controlador!',
                })
                console.log(error)
            })
    }

    saveColor = () => {
        let hsvArrayMin = this.state.newColormin.split(',')
        let hMin = hsvArrayMin[0]
        let sMin = parseInt(parseInt(hsvArrayMin[1].replace('%', '')) * 2.55)
        let vMin = parseInt(parseInt(hsvArrayMin[2].replace('%', '')) * 2.55)

        let hsvArrayMax = this.state.newColormax.split(',')
        let hMax = hsvArrayMax[0]
        let sMax = parseInt(parseInt(hsvArrayMax[1].replace('%', '')) * 2.55)
        let vMax = parseInt(parseInt(hsvArrayMax[2].replace('%', '')) * 2.55)

        let corMin = `${hMin},${sMin},${vMin}`
        let corMax = `${hMax},${sMax},${vMax}`

        const color = {
            colormin: corMin,
            colormax: corMax
        }

        axios.post(`${this.state.urlCamera}/color`, color, {timeout: 3000})
            .then(response => {
                Swal.fire({
                    icon: 'success',
                    title: 'Salvo.',
                    text: 'Limites de cores modificadas com sucesso!',
                })
            })
            .catch(error => {
                Swal.fire({
                    icon: 'error',
                    title: 'Ops.',
                    text: 'Ocorreu algum erro ao salvar os limites de cores!',
                })
            })
    }


    render() {
        return (
            <PrincipalHome>
                <Header>
                    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
                    <Logo src={LogoUrl} alt="logo" />
                    <Titulo>Sistema de dectecção de cor</Titulo>
                </Header>
                <Content>
                    <ContentCol01>
                        <VisuVideo ref={canvasA => this.canvasA = canvasA} onClick={this.getPixelColor} width="640px" height="480px"></VisuVideo>
                    </ContentCol01>
                    <ContentCol02>
                        <ContentCol02Linha01>
                            <HeaderFuncao>
                                <TituloFuncao>Limite de cores</TituloFuncao>
                            </HeaderFuncao>

                            <ButtonGreen onClick={this.startVideo}>Iniciar vídeo</ButtonGreen>
                            <ButtonBlue onClick={this.stopVideo}>Parar vídeo</ButtonBlue>
                            <MostrarRgb title="Cor mínimo" 
                                cor={this.state.corInicialMin} 
                                urlCamera={this.state.urlCamera} 
                                newColor={this.updateColormin}
                            >
                            </MostrarRgb>
                            <MostrarRgb title="Cor máximo" 
                                cor={this.state.corInicialMax}
                                urlCamera={this.state.urlCamera} 
                                newColor={this.updateColormax}
                            >
                            </MostrarRgb>
                            <ButtonBlue onClick={this.saveColor}>Salvar</ButtonBlue>
                        </ContentCol02Linha01>
                        <ContentCol02Linha02>
                            <ConfigCamera urlCamera={this.updateUrlCamera}></ConfigCamera>
                        </ContentCol02Linha02>
                    </ContentCol02>
                    <ContentCol03>
                        <ContentCol03Linha01>
                            <AjusteMascara urlCamera={this.state.urlCamera} ></AjusteMascara>
                        </ContentCol03Linha01>
                        <ContentCol03Linha02>
                            <Plc urlCamera={this.state.urlCamera}></Plc>
                        </ContentCol03Linha02>
                    </ContentCol03>
                </Content>
                <Footer>
                    <p>Todos os direitos reservados | Conecsa 2022</p>
                </Footer>
            </PrincipalHome>

        )
    }

}