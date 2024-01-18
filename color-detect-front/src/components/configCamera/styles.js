import styled from "styled-components";

export const PrincipalConfigCamera = styled.div`
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;

    align-items: center;

    width: 100%;
`;

export const Header = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center;

    width: 100%;
    height: 30px;

    background-color: #00A54F;
    color: #FFFFFF;
`;

export const Titulo = styled.h3`
    margin: 4px;
`;

export const Content = styled.div`
    display: flex;
    flex-direction: column;

    width: 100%;
`;

export const ContentLinha01 = styled.div`
    display: flex;
    flex-direction: row;

    justify-content: center;
    align-items: center;
`;

export const ContentLinha02 = styled.div`
    display: flex;
    flex-direction: row;

    justify-content: center;
    align-items: center;
`;

export const InputIp = styled.input`
    margin: 5px;

    width: 100px;
`;

export const SelectCam = styled.select`
    margin: 5px;
    
    width: 108px;
    height: 22px;
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