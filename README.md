# <center>TheSentinel</center>
<center>A Blockchain Wallet Transaction Security Platform</center>

## Description
A Secure Scanning Platform for Blockchain Wallet Transactions. <br>
**Porject Report: [Link](/static/pic/Project%20Dissertation%20Report.pdf)**<br>
Only support **Ethereum** right now

### Main Features
-   Transaction history query and visualization
    -   Data Sources: [Ethescan API](https://docs.etherscan.io/api-endpoints/accounts#get-a-list-of-normal-transactions-by-address) / [GoPlus Security API](https://docs.gopluslabs.io/reference/api-overview)
-   Blacklist address and website detection
    -   Data Source: [GoPlus Security API](https://docs.gopluslabs.io/reference/api-overview)
-   Smart contract security scanning and reporting
    -   Data Source: [Slither](https://github.com/crytic/slither)

### Example Vedio
Please Check in the Path: `static/pic/example_vedio.mp4`

## Running Environment
1.  Upper than *Python 3.10*
2.  Windows/MacOS/Linux

## Installation
1. Clone the repository.
2. Install the required dependencies by running the following command:

    ```shell
    pip3 install -r requirements.txt
    ```

## Configuration
1. Create a file named `.env` in the project root directory.
2. Open the `.env` file and add the following line:

    ```
    etherscan_api=YOUR_API_KEY
    ```

    Replace `YOUR_API_KEY` with your actual Etherscan API key.
    API key apply in https://etherscan.io/
3. If you need to change running port, open the `app.py` file and change in line 20:

    ```
    app.run(port=5008,host='0.0.0.0')
    ```

    Replace `5008` with other port.
4. Use `python3 app.py` to running the Project.
   If you want to running on background or hold a website, use `nohup python3 app.py &` in Linux system.

## System Structure
![System Structure](/static/pic/Architecture%20Diagram.png)

## System Component
![System Component](/static/pic/Component%20Diagram.png)

## Future To-do List
- [ ] Mobile Screen Adaptability Development
- [ ] Deep Tracking in Transaction Visualization 
- [ ] Support Blockchain Wallet Connection 
    - [ ] MetaMask
    - [ ] Coinbase
    - [ ] Trust Wallet
    - [ ] ....
- [ ] Muti-chain Development
- [ ] Futher User Functions Development (Subscription etc.)

## Acknowledgements List
*Not Particular Order*
-   [Ethereum](https://ethereum.org/)
-   [Ethescan](https://etherscan.io/)
-   [GoPlus Security](https://gopluslabs.io/)
-   [Newcastle University](https://www.ncl.ac.uk/)
-   My [Tutor](https://www.ncl.ac.uk/computing/staff/profile/johnfitzgerald.html) and [Supervisor](https://www.ncl.ac.uk/computing/staff/profile/essamghadafi.html)
-   [@whatly2](https://x.com/whatly2)

## Final Comment
The entire project was completed by myself, and this is the final project of my undergraduate degree at Newcastle University.