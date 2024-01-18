import { Component } from "react"
import { PrincipalConfigCamera, Header, Titulo, Content, ContentLinha01, ContentLinha02, InputIp, SelectCam, ButtonBlue } from "./styles"


export default class ConfigCamera extends Component {

    constructor (props) {
        super(props)

        this.state = {
            ipCamera: ''
        }
    }

    updateIp = (e) => {
        this.setState({
            ipCamera: e.target.value
        })
    }

    updateIpMask = (e) => {
        e.target.value = e.target.value.replace(/\D/g, "")
        e.target.value = e.target.value.replace(/(\d{3})(\d)/, "$1.$2")
        e.target.value = e.target.value.replace(/(\d{3})(\d)/, "$1.$2")
        e.target.value = e.target.value.replace(/(\d{3})(\d)/, "$1.$2")
        e.target.value = e.target.value.replace(/(\d{3})\d+?$/, "$1")

        this.setState({
            ipCamera: e.target.value
        })
    }


    conectarCamera = (e) => {
        let ipArray = this.state.ipCamera.split('.')
        let ip0 = parseInt(ipArray[0])
        let ip1 = parseInt(ipArray[1])
        let ip2 = parseInt(ipArray[2])
        let ip3 = parseInt(ipArray[3])

        const url = `http://${ip0}.${ip1}.${ip2}.${ip3}:4000/cam01`
        this.props.urlCamera(url)
    }

    render() {
        return (
            <PrincipalConfigCamera>
                <Header>
                    <Titulo>Configurações Câmera</Titulo>
                </Header>
                <Content>
                    <ContentLinha01>
                        IP:
                        <InputIp value={this.state.ipCamera} onChange={this.updateIpMask} placeholder='000.000.000.000' />
                    </ContentLinha01>
                    <ContentLinha02>
                        <ButtonBlue onClick={this.conectarCamera}>Conectar</ButtonBlue>
                    </ContentLinha02>
                </Content>
            </PrincipalConfigCamera>
        )
    }


}