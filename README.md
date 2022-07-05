import axios from "axios";
import MINTABI from "./abi/mintABI.json";
const A2P_API_PREPARE_URL = "https://a2a-api.klipwallet.com/v2/a2a/prepare";
const APP_NAME = "KLAYTN_REACT-TEST";
const to = '0x38596eD0dceaC58632bCf8BD92B5af3854d6A768';
const amount = '0.1';


const getKlipAccessUrl = (method, request_key) => {
  if (method === "QR") {
    return `https://klipwallet.com/?target=/a2a?request_key=${request_key}`;
  }
  return `kakaotalk://klipwallet/open?url=https://klipwallet.com/?target=/a2a?request_key=${request_key}`;
};

//지갑 주소 수집
export const getAddress = (setQrvalue, callback) => {
    axios
      .post(A2P_API_PREPARE_URL, {
        bapp: {
          name: APP_NAME,
        },
        type: "auth",
      })
      .then((response) => {
        const { request_key } = response.data;
        setQrvalue(getKlipAccessUrl("QR", request_key));
        let timerId = setInterval(() => {
          axios
            .get(
              `https://a2a-api.klipwallet.com/v2/a2a/result?request_key=${request_key}`
            )
            .then((res) => {
              if (res.data.result) {
                console.log(`[Result] ${JSON.stringify(res.data.result)}`);
                console.log(res.data.result);
                console.log(res.data);
                callback(res.data.result.klaytn_address);
                clearInterval(timerId);
                setQrvalue("DEFAULT");
              }
            });
        }, 1000);
      });
  };

  //klay 전송
  export const send_klay = (setQrvalue, setMyAddress) => {
    axios
      .post(A2P_API_PREPARE_URL, {
        bapp: {
          name: APP_NAME,
        },
        transaction: {
          from : setMyAddress, // optional
          to : to,
          amount : amount,
        },
        type : "send_klay",
      })
      .then((response) => {
        const { request_key } = response.data;
        setQrvalue(getKlipAccessUrl("QR", request_key));
        let timerId = setInterval(() => {
          axios
            .get(
              `https://a2a-api.klipwallet.com/v2/a2a/result?request_key=${request_key}`
            )
            .then((res) => {
              if (res.data.result) {
                console.log(res.data);
                console.log(res.data.result);
                clearInterval(timerId);
                setQrvalue("DEFAULT");
              };
            });
        }, 1000);
      })
      .catch((err)=>{
        console.log(err);
      });
};

//컨트랙트 실행

export const execute_contract = (setQrvalue, setMyAddress) => {
  axios
    .post(A2P_API_PREPARE_URL,{
      bapp: {
        name: APP_NAME,
      },
      type: "execute_contract",
      transaction : {
        from: setMyAddress, // optional
        to: "0x226d6A83e725651B48020f6A645D88c7B37005de", // contract address
        value: "100000000000000000", // 단위는 peb. 1 KLAY
        abi: {
          "constant": false,
          "inputs": [
          {
          "internalType": "uint256",
          "name": "requestedCount",
          "type": "uint256"
          }
          ],
          "name": "publicMint",
          "outputs": [],
          "payable": true,
          "stateMutability": "payable",
          "type": "function"
          },
        params: "1"
      },
    })
    .then((response) => {
      const { request_key } = response.data;
      setQrvalue(getKlipAccessUrl("QR", request_key));
      let timerId = setInterval(() => {
        axios
          .get(
            `https://a2a-api.klipwallet.com/v2/a2a/result?request_key=${request_key}`
          )
          .then((res) => {
            if (res.data.result) {
              console.log(res.data);
              console.log(res.data.result);
              clearInterval(timerId);
              setQrvalue("DEFAULT");
            };
          });
      },1000);  
    })
    .catch((err)=>{
      console.log(err);
    });
};