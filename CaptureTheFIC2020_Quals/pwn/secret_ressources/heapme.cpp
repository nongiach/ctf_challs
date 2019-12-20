#include <stdio.h>
#include <string.h>
#include <iostream>
#include <unistd.h>

class Disk
{
    public:
        char *buffer;

    public:
        Disk(size_t size) {
          buffer = new char[size];
        }
        ~Disk() {
          delete buffer;
        }
        virtual void read() {
          std::cout << "Data: " << buffer << std::endl;
          // std::cout << "Ptr: " << this << " : " << (void*) buffer << std::endl;
        }
        virtual void write() {
          std::cout << "Data: ";
          std::cin >> buffer;
        }
};

class DiskFactory
{
  private:
    Disk *disks[100] = {0};

    size_t getIndex() {
      size_t index = 0;

      do {
        std::cout << "Index: ";
        std::cin >> index;
        std::cout << index << std::endl;
      } while (index >= 100);
      return index;
    }

  public:
    void createDisk() {
      std::cout << "[+] Create Disk" << std::endl;
      std::cout << "Size: ";
      size_t size = 0;
      std::cin >> size;
      disks[getIndex()] = new Disk(size);
    }
    void readDisk() {
      std::cout << "[+] read Disk" << std::endl;
      Disk *disk = disks[getIndex()];
      if (disk)
        disk->read();
      else
        std::cout << "ERROR" << std::endl;
    }
    void writeDisk() {
      std::cout << "[+] write Disk" << std::endl;
      Disk *disk = disks[getIndex()];
      if (disk)
        disk->write();
      else
        std::cout << "ERROR" << std::endl;
    }
    void deleteDisk() {
      std::cout << "[+] delete Disk" << std::endl;
      Disk *disk = disks[getIndex()];
      if (disk)
        delete disk;
      else
        std::cout << "ERROR" << std::endl;
    }
};

class CommandManager
{
  private:
    DiskFactory disk_factory;

    size_t getCommand() {
      size_t index = 0;
      std::cout << "Command: ";
      std::cin >> index;
      return index;
    }
    void menu() {
      std::cout << "#########################################################" << std::endl;
      std::cout << "0: Create disk" << std::endl;
      std::cout << "1: Read disk" << std::endl;
      std::cout << "2: Write disk" << std::endl;
      std::cout << "3: Delete disk" << std::endl;
      std::cout << "4: Exit" << std::endl;

    }
  public:
    void loop() {
      while (true) {
        menu();
        switch (getCommand()) {
          case 0:
            disk_factory.createDisk(); break;
          case 1:
            disk_factory.readDisk(); break;
          case 2:
            disk_factory.writeDisk(); break;
          case 3:
            disk_factory.deleteDisk(); break;
          default:
            std::cout << "exit" << std::endl;
            exit(0);
        }
      }
    }
};

int main()
{
  // alarm(10);
  std::cout << "Welcome to the final stage of the CaptureTheFIC CTF by HexpressoTeam" << std::endl;
  std::cout << "Author: @chaignc" << std::endl;
  CommandManager command_manager;
  command_manager.loop();
  return 0;
}
