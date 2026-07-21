---
title: "Device farms"
tags: ["mobile-testing", "device-and-os-matrix", "track-c"]
updated: "2026-07-20"
---

# Device farms

*How cloud device farms like BrowserStack, Sauce Labs, Firebase Test Lab, and AWS Device Farm give teams on-demand access to real and virtual devices without owning or maintaining the hardware.*

> A risk-based device matrix can name twenty rows a team needs to cover, and a small team will never own,
> charge, update, and rack twenty physical phones on a shelf. The matrix was never the hard part — reaching
> the devices on it was.

> **In real life**
>
> A laundromat does not expect every household to own a machine tuned for every fabric — a delicates cycle,
> a heavy-duty industrial washer, a machine sized for a comforter. Instead, the laundromat owns the whole
> range and rents time on whichever machine the load actually needs, right when it's needed. A cloud device
> farm works the same way: instead of every team buying and maintaining its own rack of phones, it rents
> time on a shared pool that already covers far more hardware than any one team could justify owning.

**A device farm**: A device farm is a cloud service that gives on-demand, remote access to a large shared pool of real and virtual mobile devices for testing, so a team can run against many device and OS-version combinations without buying, provisioning, charging, or maintaining the physical hardware itself.

## What a device farm actually rents you

BrowserStack's App Live and App Automate give interactive and automated access to real Android and iOS
devices in the cloud — App Live for manual, hands-on sessions, App Automate for running an existing
Appium or native test suite against real hardware at scale. Sauce Labs' Real Device Cloud offers the same
kind of real-device access for both manual and automated mobile testing. Firebase Test Lab, built into the
Android developer workflow, runs your app's tests against a matrix of physical and virtual Android (and
some iOS) devices hosted by Google and reports results per device. AWS Device Farm lets you upload a
mobile app and test suite and run them across a range of real Android and iOS devices Amazon hosts and
maintains. All four remove the cost and upkeep of physical device ownership in exchange for a rented,
shared, remotely accessed pool.

> **Tip**
>
> Match the platform to the job: an interactive session (App Live, a manual Sauce Labs session) is for
> hands-on exploration and repro; an automated run (App Automate, Firebase Test Lab, AWS Device Farm) is for
> plugging an existing suite into CI so it runs against many real devices on every build.

> **Common mistake**
>
> Do not assume every device-farm session is a real physical unit. Some plans and configurations offer
> virtual devices alongside real ones — check which one a given result came from before treating it as proof
> of real-hardware behavior.

![A data center aisle with rows of tall equipment racks holding patch panels and cabling, viewed down a raised-floor walkway](device-farms.jpg)
*Datacenter Server Racks — Carl Lender, Wikimedia Commons, CC BY 2.0. [Source](https://commons.wikimedia.org/wiki/File:Datacenter_Server_Racks_(22370909788).jpg)*
- **Rented, shared infrastructure** — Nobody using this room owns a whole rack for themselves; capacity is provisioned and shared, the same principle a device farm rents out.
- **Dense, organized cabling** — Structured cabling and patch panels route traffic to many hosted units at once — the physical layer a remote device session actually rides on.
- **Rows, not a single unit** — Row after row of equipment is what lets a provider serve many customers' jobs in parallel instead of one at a time.
- **Raised floor, hidden delivery** — Power and cooling run underneath, out of sight — the operational upkeep a device-farm customer never has to think about.

**Using a device farm in a workflow**

1. **Upload the app and test suite** — Push a build and an existing Appium, Espresso, or XCUITest suite to the chosen platform.
2. **Select target devices and OS versions** — Pick rows straight from the risk-based matrix instead of whatever the farm happens to default to.
3. **Run in parallel across the pool** — Jobs queue onto available devices and execute concurrently rather than one at a time.
4. **Pull per-device results and artifacts** — Logs, screenshots, and video per device turn a pass or fail into an investigable finding.

*A device-farm job-queue parallelization simulator (Python)*

```python
available_devices = 4
jobs = [12, 8, 15, 7, 10, 9, 14, 6]
queues = [0] * available_devices
for duration in jobs:
    idx = queues.index(min(queues))
    queues[idx] += duration
serial_minutes = sum(jobs)
parallel_minutes = max(queues)
speedup = round(serial_minutes / parallel_minutes, 2)
for i, total in enumerate(queues):
    print("device_" + str(i) + "_queue_minutes=" + str(total))
print("SERIAL_MINUTES=" + str(serial_minutes))
print("PARALLEL_MINUTES=" + str(parallel_minutes))
print("SPEEDUP=" + str(speedup))
result = "PASS" if parallel_minutes < serial_minutes else "FAIL"
assert result == "PASS", "device farm parallelization did not reduce total time"
print("RESULT=" + result)
```

*A device-farm job-queue parallelization simulator (Java)*

```java
public class Main {
    public static void main(String[] args) {
        int availableDevices = 4;
        int[] jobs = {12, 8, 15, 7, 10, 9, 14, 6};
        int[] queues = new int[availableDevices];

        for (int duration : jobs) {
            int idx = 0;
            for (int i = 1; i < queues.length; i++) {
                if (queues[i] < queues[idx]) idx = i;
            }
            queues[idx] += duration;
        }

        int serialMinutes = 0;
        for (int j : jobs) serialMinutes += j;
        int parallelMinutes = queues[0];
        for (int q : queues) if (q > parallelMinutes) parallelMinutes = q;
        double speedup = Math.round((double) serialMinutes / parallelMinutes * 100) / 100.0;

        for (int i = 0; i < queues.length; i++) {
            System.out.println("device_" + i + "_queue_minutes=" + queues[i]);
        }
        System.out.println("SERIAL_MINUTES=" + serialMinutes);
        System.out.println("PARALLEL_MINUTES=" + parallelMinutes);
        System.out.println("SPEEDUP=" + speedup);
        String result = parallelMinutes < serialMinutes ? "PASS" : "FAIL";
        if (!result.equals("PASS")) throw new AssertionError("device farm parallelization did not reduce total time");
        System.out.println("RESULT=" + result);
    }
}
```

### Your first time: Run one suite on a device farm

- [ ] Pick a platform for the job at hand — Interactive access (App Live, a manual Sauce Labs session) for exploration; automated access (App Automate, Firebase Test Lab, AWS Device Farm) for CI.
- [ ] Upload the app build and existing test suite — Reuse an existing Appium, Espresso, or XCUITest suite rather than writing device-farm-specific tests.
- [ ] Choose devices straight from the risk-based matrix — Select the rows the matrix already justified instead of a platform's default device list.
- [ ] Review per-device logs and artifacts — Confirm whether a failure is device-specific or reproduces everywhere in the run.

- **A test passes locally but fails only on the device farm.**
  Check network conditions, app-signing configuration, and whether the farm session is a real device or a virtual one before assuming the test itself is wrong.
- **Runs queue for a long time before starting.**
  Check plan-level concurrency limits; the pool is shared across customers, and a low concurrency allowance serializes jobs that should run in parallel.
- **A result can't be reproduced locally.**
  Pull the device farm's logs, screenshots, and session video for that exact device and OS version rather than guessing from the failure message alone.

### Where to check

- Each platform's supported-device list and current OS-version coverage before assuming a row is available.
- Per-device logs, screenshots, and session recordings the platform captures for each run.
- Plan-level concurrency limits, since they determine how much of the matrix actually runs in parallel.
- [[mobile-testing/device-and-os-matrix/building-a-matrix]] for the risk-based device list a farm run should be validating against.

### Worked example: a matrix that only became testable through a device farm

1. A risk-based matrix names twelve device/OS-version rows the team has no physical way to own.
2. The team uploads its Appium suite to a cloud device farm and maps each matrix row to an available real
   device on the platform.
3. The suite runs across all twelve in parallel instead of queuing serially on a handful of owned phones.
4. One row fails only on a specific OEM skin; the session video and logs from that exact device let the
   team reproduce and fix the issue without ever owning that phone.

**Quiz.** What is the core value a cloud device farm provides over owning physical devices?

- [ ] It replaces the need for a risk-based device matrix entirely
- [ ] It guarantees every session runs on a real physical device with no exceptions
- [x] It gives on-demand, shared, remote access to many device and OS-version combinations without the cost and upkeep of owning them
- [ ] It only supports automated tests, never interactive manual sessions

*The core value is rented, shared access to hardware and OS-version coverage a team would otherwise have to buy and maintain itself; it still relies on the matrix to know which rows to request.*

- **BrowserStack App Live vs App Automate** — App Live is interactive manual sessions on real devices; App Automate runs an existing automated suite against real devices at scale.
- **Firebase Test Lab** — Google's cloud testing infrastructure that runs an app's tests across a matrix of physical and virtual Android (and some iOS) devices.
- **AWS Device Farm** — Amazon's service for uploading a mobile app and test suite to run across a range of real Android and iOS devices Amazon hosts.

### Challenge

Take three rows from a risk-based device matrix and map each one to a specific real-device option on a cloud device farm platform of your choice.

- [BrowserStack — App Automate](https://www.browserstack.com/app-automate)
- [Sauce Labs — Real Device Cloud](https://saucelabs.com/products/mobile-testing/real-device-cloud)
- [Firebase — Test Lab Documentation](https://firebase.google.com/docs/test-lab)
- [AWS Device Farm](https://aws.amazon.com/device-farm/)
- [Amazon Web Services — Introduction to AWS Device Farm](https://www.youtube.com/watch?v=UiJo_PEZkD4)

🎬 [Introduction to AWS Device Farm](https://www.youtube.com/watch?v=UiJo_PEZkD4) (6 min)

- A device farm rents shared, remote access to real and virtual devices instead of requiring physical ownership.
- BrowserStack, Sauce Labs, Firebase Test Lab, and AWS Device Farm each offer real-device access with different interactive and automated workflows.
- Match interactive platforms to exploration and repro, and automated platforms to CI-driven suite runs.
- A device farm makes a risk-based matrix actually testable by supplying the hardware the matrix names.


## Related notes

- [[Notes/mobile-testing/device-and-os-matrix/fragmentation|Fragmentation]]
- [[Notes/mobile-testing/device-and-os-matrix/building-a-matrix|Building a matrix]]
- [[Notes/mobile-testing/device-and-os-matrix/real-vs-emulated|Real vs emulated]]


---
_Source: `packages/curriculum/content/notes/mobile-testing/device-and-os-matrix/device-farms.mdx`_
