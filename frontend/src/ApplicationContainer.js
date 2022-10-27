import { useState } from "react";
import ApplicationList from "./ApplicationList";


const ApplicationContainer = () => {
  const [apps, setApps] = useState([
    {
      "description": "This application provides alpha services.",
      "eks_size": "xl",
      "name": "aplha",
      "owner": "john.doe@trdebyte.com",
      "stack": "python-django",
      "team": "Unicorn",
      "version": "1.2.0"
    },
    {
      "description": "This application provides beta services. on top of alpha",
      "eks_size": "m",
      "name": "beta",
      "owner": "max.mustermann@trdebyte.com",
      "stack": "java-spring",
      "team": "Duck",
      "version": "1.0.0"
    }
  ]
  )
  return (
    <div className="container">
     <ApplicationList apps={apps} />
    </div>
  );
}
 
export default ApplicationContainer;
