---
title: "A Template for System Design"
date: 2023-06-22
tags:
  - learnings
  - system-design
---

Designing a software system is difficult, especially when you don't have a plan or a set of instructions. But once you have a plan to guide you, it becomes easier to solve the problem step by step. In this blog, I will share a few things I learned from reading online and my own experience about how to approach system design questions at work or in interviews.


## Problem statement

To begin, it is important to accurately define the problem statement. This involves providing context about the problem and explaining the reasons for solving it. It is crucial to address the "why" behind the problem, including its consequences and impact.

When writing a technical design document, it is beneficial to offer background information and discuss existing solutions. This helps to provide a comprehensive understanding of the problem and its current state.

Lastly, it is helpful to briefly describe the desired outcome of the tech document or system design. By implementing the proposed solution, users will no longer encounter the previously mentioned issue.

## Listing Down Assumptions

This step is important for setting the right expectations. When you start building something, there are certain things you assume to be true. Here are a couple of examples:

1. For instance, let's say your design relies on using specific tools like Kubernetes (k8s) or AWS, as it needs to utilize their internal features.
2. Another example could be if a company has its own ongoing architecture development. In your design, you assume that your solution will work only if that specific architecture is in place.

By stating these assumptions from the beginning, it ensures that everyone understands what is needed and what limitations exist for the project.

## Risk and Open Items

In this step, you outline the challenges or potential issues that your project may encounter. Since assumptions were made in the previous steps, there are some associated risks, such as:

1. The API you rely on might lack proper documentation or support. This could result in project delays and difficulties in implementing your solution. 
2. An "open item" refers to any pending work that needs to be completed before you can begin working on your project. It acts as a prerequisite or dependency for your project to progress.


By identifying and acknowledging these challenges and open items, you can plan for them in advance and mitigate any setbacks or obstacles that may arise during the project.
 
## High Level Design

In this step, you will create a basic diagram that outlines the main components of your system and how they interact. The diagram provides a high-level overview without going into too much details, helping stakeholders visualize the overall architecture and information flow. Focus on the major components and their interactions, keeping it simple and straightforward.

## High Level Description

In this step, you will describe your solution using the components identified in the high-level design. For example, if your solution is a web application, you would explain how a request flows through your design and generates a response. This involves explaining the purpose and functionality of each individual component.


Now that you have a basic working solution, it is crucial to evaluate its robustness before seeking feedback. Take a moment to consider various scenarios and error situations that could potentially disrupt your design. By proactively identifying and addressing these issues, you demonstrate thoroughness and preparedness when sharing your design with others. This approach prevents wasting others' time by avoiding glaring issues that may arise, such as handling excessive requests. By anticipating and resolving potential problems beforehand, you can present a more robust and reliable design to receive valuable feedback.
 
To refine your design, you can follow the steps below:

- Consider the possibility of data inconsistency or an inconsistent system state due to failures or errors. Determine if you need to implement transactions or a SAGA (Saga pattern) to maintain data integrity and consistency.
- Address the risk of creating duplicate records in your system. Ensure that appropriate measures are in place to prevent the creation of duplicate entries.
- Evaluate how your system will handle database loads. Consider both read-heavy and write-heavy scenarios and design strategies to efficiently handle these workloads.    
    - For read-heavy scenarios, implement caching mechanisms to reduce database load and improve response times.
    - For write-heavy scenarios, use techniques like sharding or partitioning, or consider implementing asynchronous processing to handle high write volumes.
- Plan for potential database crashes, both primary and secondary instances. Establish backup and recovery mechanisms to ensure data integrity and minimize downtime.
- If your design includes caching, consider the possibility of cache failures or crashes. Implement fault-tolerant caching mechanisms to avoid such failures.
- Think about the impact of increased server load beyond anticipated levels. Design your system to handle scalability by implementing strategies like horizontal scaling, load balancing, and rate-limiting to ensure optimal performance under high load conditions.
- Think about the possibility of web server or application server crashes. Implement redundancy and failover mechanisms to provide HA(high availability).
- Address any potential latency issues in your system. Optimize network communication, database querie to minimize response times.
- valuate whether all operations in your system need to be synchronous. Explore opportunities to make certain operations asynchronous to improve system responsiveness and scalability.
- Identify any performance bottlenecks and find ways to make your system faster. Optimize algorithms, improve database indexing, utilize caching techniques etc.

Once your design has been refined, please share the design document with your peers to gather their feedback. However, it is important not to rush the process of creating the document. It is recommended to allocate a minimum of one week for designing the document, and it is advised not to settle for less time.

When refining your design to handle potential error scenarios, it is crucial to avoid imagining non-existent problems or scenarios that are unlikely to occur. By doing so, you can prevent the creation of overly complex and potentially costly designs that are unnecessary. It is important to consider the trade-offs and not strive for perfection. As long as your solution delivers the intended features and does not inconvenience the user, it is considered good enough. Avoid incorporating fancy patterns or technologies merely for the sake of it.

## Low Level Design

Once done, start working on low level design. This would involve:

1. Desribing invidual components or modules.
2. Design API interface.
3. Writing down sequence diagram to show how these components describe.

## Come up with Milestones

Milestones serve as checkpoints to showcase the progress and achievements of a project. Each milestone represents a significant deliverable that marks a specific stage of completion. Here are some examples of milestones in the context of software development:

1. Gathering the requirements.
2. Designign the high level solution and reviewing
3. Implementing modules as described in the low level design. 

## Deployment details

If the company already has a common deployment strategy in place, it is possible to skip the deployment section as it aligns with the existing practices. However, if it is a hobby or personal project where no established deployment strategy exists, it becomes important to describe how the designed solution will be deployed.


I hope these guidlines will help you to streamline your thoughts while designing the system and also helps you to build robust systems.