import { Component } from "react";
import Swal from "sweetalert2";

import {
  PrincipalHome,
  Header,
  VisuVideo,
  ButtonGreen,
  ButtonBlue,
  Logo,
  Titulo,
  Footer,
  Content,
  ContentCol01,
  ContentCol02,
  ContentCol03,
  ContentCol02Linha01,
  ContentCol02Linha02,
  ContentCol03Linha01,
  ContentCol03Linha02,
  TituloFuncao,
  HeaderFuncao,
  ContentCol02Linha03,
} from "./styles";

import AjusteMascara from "../ajusteMascara/AjusteMascara";
import ConfigCamera from "../configCamera/configCamera";
import Plc from "../plc/Plc";
import axios from "axios";
import MostrarRgb from "../mostraRgb/MostraRgb";

import LogoUrl from "../../images/logo.png";

export default class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {
      urlCamera: "",
      urlCameraAux01: "",
      urlCameraAux02: "",
      corInicialMin: "255,255,255",
      corInicialMax: "255,255,255",
      newColormin: "",
      newColormax: "",
      getColorsCalled: false,
    };

    this.urlFrame = this.state.urlCamera;
  }

  drawImage = (img, x, y) => {
    this.contexto.drawImage(img, x, y);
  };

  componentDidMount() {
    this.contexto = this.canvasA.getContext("2d");
  }

  async componentDidUpdate() {
    if (!this.state.getColorsCalled) {
      await this.getColors();
      this.setState({ getColorsCalled: true });
    }
  }

  getFrame = async () => {
    var img = new Image();
    img.crossOrigin = "Anonymous";
    img.src = this.state.urlCameraAux01;

    img.onload = () => {
      img.src = this.state.urlCameraAux01;
      this.drawImage(img, 0, 0);
    };
  };

  rgb2hsv = (r, g, b) => {
    var computedH = 0;
    var computedS = 0;
    var computedV = 0;

    //remove spaces from input RGB values, convert to int
    r = parseInt(("" + r).replace(/\s/g, ""), 10);
    g = parseInt(("" + g).replace(/\s/g, ""), 10);
    b = parseInt(("" + b).replace(/\s/g, ""), 10);

    if (
      r === null ||
      g === null ||
      b === null ||
      isNaN(r) ||
      isNaN(g) ||
      isNaN(b)
    ) {
      Swal.fire({
        icon: "error",
        title: "Ops.",
        text: "Por favor, informe valores RGB válidos.",
      });

      return;
    }
    if (r < 0 || g < 0 || b < 0 || r > 255 || g > 255 || b > 255) {
      Swal.fire({
        icon: "error",
        title: "Ops.",
        text: "Por favor, informe valores RGB válidos.",
      });
      return;
    }
    r = r / 255;
    g = g / 255;
    b = b / 255;
    var minRGB = Math.min(r, Math.min(g, b));
    var maxRGB = Math.max(r, Math.max(g, b));

    // Black-gray-white
    if (minRGB === maxRGB) {
      computedV = minRGB;
      return [0, 0, computedV];
    }

    // Colors other than black-gray-white:
    var d = r === minRGB ? g - b : b === minRGB ? r - g : b - r;
    var h = r === minRGB ? 3 : b === minRGB ? 1 : 5;
    computedH = 60 * (h - d / (maxRGB - minRGB));
    computedS = ((maxRGB - minRGB) / maxRGB) * 100;
    computedV = maxRGB * 100;
    return [parseInt(computedH), parseInt(computedS), parseInt(computedV)];
  };

  getPixelColor = (e) => {
    e.preventDefault();

    if (this.contexto.getImageData) {
      const { data } = this.contexto.getImageData(
        e.nativeEvent.offsetX,
        e.nativeEvent.offsetY,
        1,
        1
      );

      let hsv = this.rgb2hsv(data[0], data[1], data[2]);

      const cor = `${hsv[0]}, ${hsv[1]}%, ${hsv[2]}%`;

      this.setState({
        corInicialMin: cor,
        corInicialMax: cor,
        newColormin: cor,
        newColormax: cor,
      });
    }
  };

  updateIputs = (e) => {
    switch (e.target.name) {
      case "corInicialMin":
        this.setState({ corInicialMin: e.target.value });
        break;
      case "corInicialMax":
        this.setState({ corInicialMax: e.target.value });
        break;
      case "newColormin":
        this.setState({ newColormin: e.target.value });
        break;
      case "newColormax":
        this.setState({ newColormax: e.target.value });
        break;
      default:
        break;
    }
  };

  updateColormin = (newColor) => {
    this.setState({
      newColormin: newColor,
    });
  };

  updateColormax = (newColor) => {
    this.setState({
      newColormax: newColor,
    });
  };

  newColor = async (cor) => {
    try {
      await axios.post(`${this.state.urlCamera}/colors`, { cor });
      this.getColors();
    } catch (error) {
      Swal.fire({
        icon: "error",
        title: "Erro",
        text: "Erro ao atualizar a cor",
      });
    }
  };

  getColors = async () => {
    if (this.state.urlCamera === "") {
      return;
    }

    let ip0 = this.state.urlCamera.split(".")[0].replace("http://", "");
    let ip1 = this.state.urlCamera.split(".")[1];
    let ip2 = this.state.urlCamera.split(".")[2];
    let ip3 = this.state.urlCamera.split(".")[3];

    await axios
      .get(`http://${ip0}.${ip1}.${ip2}.${ip3}/color`, { timeout: 3000 })
      .then((response) => {
        let data = response.data;
        if (data) {
          console.log(data);
          let limitMin = data.color.colormin.split(",");
          let limitMax = data.color.colormax.split(",");
          let sMin = parseInt(parseInt(limitMin[1]) / 2.55);
          let vMin = parseInt(parseInt(limitMin[2]) / 2.55);
          let sMax = parseInt(parseInt(limitMax[1]) / 2.55);
          let vMax = parseInt(parseInt(limitMax[2]) / 2.55);

          this.setState({
            corInicialMin: `${limitMin[0]},${sMin}%,${vMin}%`,
            corInicialMax: `${limitMax[0]},${sMax}%,${vMax}%`,
            newColormin: `${limitMin[0]},${sMin}%,${vMin}%`,
            newColormax: `${limitMax[0]},${sMax}%,${vMax}%`,
          });
        }
      })
      .catch((error) => {
        let message = `Ocorreu um erro ao carregar as cores.\nTente novamente. ${error}`;
        if (error.status === 400 || error.status === 500) {
          message = error.data.error;
        } else if (error.status === 404) {
          message = error.data.message;
        }
        Swal.fire({
          icon: "error",
          title: "Ops.",
          text: message,
        });
      });
  };

  saveColor = async () => {
    if (this.state.newColormin === "") {
      Swal.fire({
        icon: "error",
        title: "Não permitido!",
        text: "É necessário conectar-se à um controlador para realizar esta ação.",
      });

      return;
    }
    this.stopVideo();
    let hsvArrayMin = this.state.newColormin.split(",");
    let hMin = hsvArrayMin[0];
    let sMin = parseInt(parseInt(hsvArrayMin[1].replace("%", "")) * 2.55);
    let vMin = parseInt(parseInt(hsvArrayMin[2].replace("%", "")) * 2.55);

    let hsvArrayMax = this.state.newColormax.split(",");
    let hMax = hsvArrayMax[0];
    let sMax = parseInt(parseInt(hsvArrayMax[1].replace("%", "")) * 2.55);
    let vMax = parseInt(parseInt(hsvArrayMax[2].replace("%", "")) * 2.55);

    let corMin = `${hMin},${sMin},${vMin}`;
    let corMax = `${hMax},${sMax},${vMax}`;

    const color = {
      colormin: corMin,
      colormax: corMax,
    };

    await axios
      .post(`${this.state.urlCamera}/color`, color, { timeout: 3000 })
      .then((response) => {
        Swal.fire({
          icon: "success",
          title: "Salvo.",
          text: response.data.message,
        });
        this.startVideo();
      })
      .catch((error) => {
        let message = `Ocorreu um erro ao salvar o limite de cores.\n Tente novamente. ${error}`;
        if (error.status === 400 || error.status === 500) {
          message = error.data.error;
        } else if (error.status === 404) {
          message = error.data.message;
        }
        Swal.fire({
          icon: "error",
          title: "Ops.",
          text: message,
        });
      });
  };

  startVideo = () => {
    if (this.state.urlCamera === "") {
      Swal.fire({
        icon: "error",
        title: "Não permitido!",
        text: "Você precisa conectar um controlador antes de iniciar o vídeo!",
      });
      return;
    }
    this.setState(
      {
        urlCameraAux01: this.state.urlCameraAux02,
      },
      () => {
        this.getFrame();
        this.getFrame();
      }
    );
  };

  stopVideo = () => {
    if (this.state.urlCamera === "") {
      Swal.fire({
        icon: "error",
        title: "Não permitido!",
        text: "Nenhum vídeo foi detectado!",
      });
      return;
    }
    this.setState({
      urlCameraAux01: "",
    });
  };

  updateUrlCamera = async (urlCamera) => {
    this.setState({
      urlCamera: urlCamera,
      urlCameraAux01: urlCamera,
      urlCameraAux02: urlCamera,
    });

    Promise.all([
      AjusteMascara.getDerivedStateFromProps(this.props, this.state),
      Plc.getDerivedStateFromProps(this.props, this.state),
      this.getFrame()
    ]).then(() => {
      Swal.fire({
        icon: "success",
        title: "Conectado.",
        text: "Conectado ao controlador com sucesso!\n Inicie o vídeo para realizar a calibração.",
      });
    });
  };

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
            <VisuVideo
              ref={(canvasA) => (this.canvasA = canvasA)}
              onDoubleClick={this.getPixelColor}
              width="640px"
              height="480px"
            ></VisuVideo>
          </ContentCol01>
          <ContentCol02>
            <ContentCol02Linha01>
            <HeaderFuncao>
                <TituloFuncao>Vídeo</TituloFuncao>
              </HeaderFuncao>
              <ButtonGreen onClick={this.startVideo}>Iniciar vídeo</ButtonGreen>
              <ButtonBlue onClick={this.stopVideo}>Parar vídeo</ButtonBlue>
            </ContentCol02Linha01>
            <ContentCol02Linha01>
              <HeaderFuncao>
                <TituloFuncao>Limite de cores</TituloFuncao>
              </HeaderFuncao>
              <MostrarRgb
                title="Cor mínimo"
                cor={this.state.corInicialMin}
                urlCamera={this.state.urlCamera}
                newColor={this.updateColormin}
              ></MostrarRgb>
              <MostrarRgb
                title="Cor máximo"
                cor={this.state.corInicialMax}
                urlCamera={this.state.urlCamera}
                newColor={this.updateColormax}
              ></MostrarRgb>
              <ButtonBlue onClick={this.saveColor}>Salvar</ButtonBlue>
            </ContentCol02Linha01>
            <ContentCol02Linha02>
              <ConfigCamera urlCamera={this.updateUrlCamera}></ConfigCamera>
            </ContentCol02Linha02>
          </ContentCol02>
          <ContentCol03>
            <ContentCol03Linha01>
              <AjusteMascara urlCamera={this.state.urlCamera}></AjusteMascara>
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
    );
  }
}
