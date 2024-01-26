import axios from "axios";
import { Component } from "react";
import Swal from "sweetalert2";
import {
  PrincipalPlc,
  Header,
  Titulo,
  Content,
  ContentLinha01,
  ContentLinha02,
  ContentLinha03,
  InputIp,
  Select,
  ButtonBlue,
  InputDbNumber,
  InputBit,
} from "./styles";

export default class Plc extends Component {
  constructor(props) {
    super(props);

    this.state = {
      ipPlc: "",
      value: "",
      rack: 0,
      slot: 1,
      db: 0,
      bit: 0,
      urlCamera: "",
    };
  }

  componentWillReceiveProps = (props) => {
    this.setState({
      urlCamera: props.urlCamera,
    });

    this.getPlc();
  }

  updateIpMask = (e) => {
    //e.target.value = e.target.value.replace(/\D/g, "")
    //e.target.value = e.target.value.replace(/(\d{3})(\d)/, "$1.$2")
    //e.target.value = e.target.value.replace(/(\d{3})(\d)/, "$1.$2")
    //e.target.value = e.target.value.replace(/(\d{3})(\d)/, "$1.$2")
    //e.target.value = e.target.value.replace(/(\d{3})\d+?$/, "$1")

    this.setState({
      ipPlc: e.target.value,
    });
  }

  updateIp = (e) => {
    this.setState({
      value: e.target.value,
    });
  }

  updateRack = (e) => {
    this.setState({
      rack: e.target.value,
    });
  }

  updateSlot = (e) => {
    this.setState({
      slot: e.target.value,
    });
  }

  updateDb = (e) => {
    this.setState({
      db: e.target.value,
    });
  }

  updateBit = (e) => {
    this.setState({
      bit: e.target.value,
    });
  }

  getPlc = () => {
    axios
      .get(`http://127.0.0.1:4000/cam01/plc`, { timeout: 3000 })
      .then((response) => {
        let data = response.data;
        if (data) {
          let [db, bit] = data.plc.var_cam.split(",");

          this.setState({
            ipPlc: data.plc.ip,
            rack: data.plc.rack,
            slot: data.plc.slot,
            db: db,
            bit: bit,
          });
        }
      })
      .catch((error) => {});
  }

  savePlc = () => {
    if (this.state.urlCamera === "") {
      Swal.fire({
        icon: "error",
        title: "Não permitido!",
        text: "É necessário conectar-se à um controlador para realizar esta ação.",
      });

      return;
    }
    let plc = {
      ip: this.state.ipPlc,
      rack: this.state.rack,
      slot: this.state.slot,
      var_cam: `${this.state.db},${this.state.bit}`,
    };
    axios
      .post(`http://127.0.0.1:4000/cam01/plc`, plc, { timeout: 3000 })
      .then((response) => {
        Swal.fire({
          icon: "success",
          title: "Salvo.",
          text: "PLC salvo com sucesso!",
        });
      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "Ops.",
          text: "Ocorreu algum erro ao salvar o PLC!",
        });
      });
  }

  render() {
    return (
      <PrincipalPlc>
        <Header>
          <Titulo>Configurações PLC</Titulo>
        </Header>
        <Content>
          <ContentLinha01>
            IP:
            <InputIp
              value={this.state.ipPlc}
              onChange={this.updateIpMask}
              placeholder="000.000.000.000"
            />
            Rack:
            <Select value={this.state.rack} onChange={this.updateRack}>
              <option value={0}>0</option>
              <option value={1}>1</option>
            </Select>
            Slot:
            <Select value={this.state.rack} onChange={this.updateSlot}>
              <option value={1}>1</option>
              <option value={2}>2</option>
            </Select>
          </ContentLinha01>
          <ContentLinha02>
            DB:
            <InputDbNumber
              value={this.state.db}
              onChange={this.updateDb}
            ></InputDbNumber>
            Bit:
            <InputBit
              value={this.state.bit}
              onChange={this.updateBit}
            ></InputBit>
          </ContentLinha02>
          <ContentLinha03>
            <ButtonBlue onClick={this.savePlc}>Salvar PLC</ButtonBlue>
          </ContentLinha03>
        </Content>
      </PrincipalPlc>
    );
  }
}
