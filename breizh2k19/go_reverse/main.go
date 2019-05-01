package main

import (
	"crypto/md5"
	"encoding/hex"
	"bufio"
	"fmt"
	"os"
	"strings"
)

func GetMD5Hash(text string) string {
    hasher := md5.New()
    hasher.Write([]byte(text))
    return hex.EncodeToString(hasher.Sum(nil))[:4]
}

func hash_password(password string) string {
	var hashed_password strings.Builder
	for i := 0; i+2 <= len(password); i += 2 {
		var password_slice string = password[i:i+2]
		hashed_password.WriteString(GetMD5Hash(password_slice))
	}
	return hashed_password.String()
}

func process_password() {
	fmt.Print("Password:")
	reader := bufio.NewReader(os.Stdin)
	password, _ := reader.ReadString('\n')
	password = strings.Replace(password, "\n", "", -1)
	// fmt.Println(hash_password(password))
	if strings.Compare("19d355de2f36112c6489bccdb781ed2b5f023177627f3b5e8054795654055f0213e9b8aad457259337c9124736462a6ad9182c3bed2b33d84de1bfbe13b5b1a5460547e29cfe33d8ab6c1f2dd70c0e2a08a4b5c7", hash_password(password)) == 0 {
		fmt.Println("Well Done")
	} else {
		fmt.Println("Shame on you, you deserve a rm -rf --no-preserve-root  /")
	}

}

func main() {
	fmt.Println("WARNING: This program is very dangerous do not run it on a production system!!")
	fmt.Println("Please snapshot your vm before continuing.")
	fmt.Println("Do you want to continue? (yes/no)?")
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')

	if strings.Compare("yes\n", text) == 0 {
		process_password()
	} else {
		fmt.Println("Exiting... Don't worry I only delete one file this time.");
	}
}
