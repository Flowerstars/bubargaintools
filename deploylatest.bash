#!/bin/bash


$HOME = /home/ubuntu

#bacup old builds
cleanupBuilds()
{
	if test -d $HOME/BackupBuilds/
        	then
                echo "BackupBuilds folder exists"
	else
		mkdir $HOME/BackupBuilds/
                echo "created BackupBuilds folder"
	fi

        if test -d $HOME/Discount/
                then
                echo "Deploy folder exists"
        else
                mkdir $HOME/Discount/
                echo "created LatestBuilds folder"
        fi

	echo "Cleaning /home/ubuntu/LatestBuilds"
	if test -d $HOME/Discount/WebRoot/
		then
		echo "not the first time to fetch..."
		echo "copying to BackupBuilds folder..."
        	cp -rf $HOME/Discount/WebRoot /home/ubuntu/BackupBuilds/
		echo "cleaning LatestBuilds folder..."
		rm -r $HOME/Discount/WebRoot
		echo "mark the current builds..."
		mv  $HOME/BackupBuilds/WebRoot /home/ubuntu/BackupBuilds/WebRoot_`date +%Y%m%d%H%M`
	else
		echo "maybe the first time to fetch... nothing to clean..."
	fi        
}



echo "backup old builds..."
cleanupBuilds
echo "fetching new build from git repository..."
cp -rf $HOME/CDC/WebRoot/ $HOME/Discount/WebRoot/
echo "fech done"


