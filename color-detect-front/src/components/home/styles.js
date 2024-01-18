import styled from "styled-components";

export const PrincipalHome = styled.div`
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
`;

export const Header = styled.div`
    display: flex;
    flex-wrap: wrap;
    align-items: center;

    background-color: #0a365e;
    color: #00a54f;

    border-bottom-style: solid;
    border-bottom-width: 2px;
    border-color: #0a365e;
    
    margin-bottom: 5px;

    height: 70px;
`;

export const Content = styled.div`
    display: flex;
`;


export const ContentCol01 = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
`;

export const ContentCol02 = styled.div`
    display: flex;
    flex-direction: column;

    margin-left: 3px;

    width: 350px;
`;

export const ContentCol03 = styled.div`
    display: flex;
    flex-direction: column;

    margin-left: 3px;
`;

export const Footer = styled.div`
    display: flex;
    align-items: center;

    background-color: #0a365e;

    p{
        color: #00a54f;
        margin-left: 10px;
    }

    height: 30px;
    margin-top: 5px;
`;

export const Logo = styled.img`
    display: flex;

    width: 200px;
    height: 43px;
`;

export const Titulo = styled.h1`
    display: flex;
`;

export const VisuVideo = styled.canvas`
    display: flex;
    align-items: center;
    justify-content: center;

    border-style: solid;
    border-width: 2px;
    border-radius: 5px;
    border-color: #0a365e;
    border-bottom-width: 12px;
    border-top-width: 12px;

    cursor: crosshair;
`;

export const ContentCol02Linha01 = styled.div`
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;

    align-items: center;

    border-style: solid;
    border-radius: 5px;
    border-width: 4px;
    border-color: #00A54F;

    margin-bottom: 2px;
`;

export const ContentCol02Linha02 = styled.div`
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;

    align-items: center;

    border-style: solid;
    border-radius: 5px;
    border-width: 4px;
    border-color: #00A54F;
`;

export const ContentCol03Linha01 = styled.div`
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;

    align-items: center;

    border-style: solid;
    border-radius: 5px;
    border-width: 4px;
    border-color: #00A54F;

    margin-bottom: 2px;
`;

export const ContentCol03Linha02 = styled.div`
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;

    align-items: center;

    border-style: solid;
    border-radius: 5px;
    border-width: 4px;
    border-color: #00A54F;
`;

export const HeaderFuncao = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;

    width: 100%;
    height: 30px;

    background-color: #00A54F;
    color: #FFFFFF;
`;

export const TituloFuncao = styled.h3`
    margin: 4px;
`;

export const ButtonGreen = styled.button`
    background-color: #00a54f;
    border-color: #00a54f;
    color: #fff;
    border-style: solid;
    border-radius: 3px;

    width: 90%;
    height: 40px;

    cursor: pointer;

    margin: 5px;
`;

export const ButtonBlue = styled.button`
    background-color: #0a365e;
    border-color: #0a365e;
    color: #fff;
    border-style: solid;
    border-radius: 3px;

    width: 90%;
    height: 40px;

    cursor: pointer;

    margin: 5px;
`;
