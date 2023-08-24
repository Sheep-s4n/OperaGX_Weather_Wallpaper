function themeInstallation(){
    try {
        const id = document.querySelector('meta[property="aoc:app_id"]').content;
        chrome.addonsPrivate.installTheme(id , (err) => 
        {
            if (err) 
            {
                console.log("Failed to install theme !");
                console.log(`Error: ${err}`);
            } 
            else
            {
                console.log("Successfuly installed theme !");
            }
        });
        console.log("Successfuly runned function");
        return true;

    } catch (err) { 
        return false;
    }
}

intervalId = window.setInterval(function(){
    suceed = themeInstallation();
    if (suceed) {
        clearInterval(intervalId);
        window.close();
    };
}, 300);