package main

import (
	"fmt"
	"io/ioutil"

	"gopkg.in/yaml.v2"
)

/*type Config struct {
	Name        string
	Type        string
	Source      string
	Destination string
	Excludes    string
	Bandwidth   string
	Commands    string
}*/
type Config struct {
	Attr struct {
		Type        string
		Source      string
		Destination string
		Excludes    []string
		Bandwidth   string
		Commands    string
	}
}

func main() {
	var config Config
	//var command string

	//filename, _ := filepath.Abs("conf.yml")
	yamlFile, err := ioutil.ReadFile("conf.yaml")
	check(err)

	err = yaml.Unmarshal(yamlFile, &config)
	check(err)
	//command := "rclone --config /home/a.zhideev/rclone/rclone.conf --log-file=/var/log/rclone --log-level INFO", config.Type, " ", config.Source, " + nxs:", config.Destination
	fmt.Println("rclone --config /home/a.zhideev/rclone/rclone.conf --log-file=/var/log/rclone --log-level INFO " + config.Attr.Type + " " + config.Attr.Source + config.Attr.Excludes + " nxs:" + config.Attr.Destination)
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}
